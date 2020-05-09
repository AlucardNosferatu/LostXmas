import time
import jieba
import os
import sys
import synonyms
import random
import numpy as np
from py2neo import Graph, Node, Relationship, walk, NodeMatcher
from scipy.linalg import norm
from snownlp import SnowNLP
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
import seq2seq.word.test_model_word as test_model_word
import seq2seq.phrase.test_model_phrase as test_model_phrase
import seq2seq.word.train_word as train_word


def tf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator / denominator


def load_data():
    root_path = os.path.dirname(sys.path[0])
    os.chdir(root_path)
    sentences = 'seq2seq\\word\\data\\test.txt'
    stopwords = 'ChatterBot\\stopwords.txt'
    conversation_list = open(sentences, encoding='UTF-8').read().split('\n')
    conversation_pairs = []
    for i in tqdm(range(0, len(conversation_list), 2)):
        conversation = [conversation_list[i], conversation_list[i + 1]]
        conversation_pairs.append(conversation)
    stopwords_list = open(stopwords, encoding='UTF-8').read().split('\n')
    time.sleep(2)
    return conversation_pairs, stopwords_list


def talk_loop_deprecated():
    conversation_pairs, stopwords_list = load_data()
    hint = '说些什么\n'
    while True:
        print(talk_once_deprecated(conversation_pairs, stopwords_list, hint))
        hint = ''


def talk_once_deprecated(conversation_pairs, stopwords_list, hint='说些什么\n'):
    input_str = input(hint)
    words = jieba.lcut(input_str)
    words = list(set(words))
    # remove stopwords
    if len(words) > 4:
        for each in stopwords_list:
            for word in words:
                if word == each:
                    words.remove(word)
    # query every key words
    all_candidates = {}
    for word in words:
        candidate_indices = []
        print("\n" + word + ":")
        for i in tqdm(range(0, len(conversation_pairs))):
            if word in conversation_pairs[i][0]:
                candidate_indices.append(i)
        all_candidates[word] = candidate_indices

    score = 0
    key_word = ''
    similar_str = ''
    candidate_str = ''
    for each in all_candidates:
        print("\n" + each + ":")
        for each_sentence in tqdm(all_candidates[each]):
            temp = jaccard_similarity(conversation_pairs[each_sentence][0], input_str)
            if temp > score:
                score = temp
                key_word = each
                candidate_str = conversation_pairs[each_sentence][1]
                similar_str = conversation_pairs[each_sentence][0]
    # print(score)
    if score > 0.5:
        # print(key_word)
        # print(similar_str)
        if random.choice([True, False]):
            return candidate_str
        else:
            output_words = jieba.lcut(candidate_str)
            for each in output_words:
                syn = synonyms.nearby(each)
                temp = 0
                temp_str = each
                print("\n" + each + ":")
                for i in tqdm(range(1, len(syn[1]))):
                    if syn[1][i] > 0.76:
                        if temp < syn[1][i]:
                            if temp_str not in syn[0][i]:
                                temp = syn[1][i]
                                candidate_str = candidate_str.replace(temp_str, syn[0][i])
                                temp_str = syn[0][i]
            return candidate_str
    else:
        return test_model_word.TulpaAvatar(input_str)


def syn_replace(input_str):
    input_words = jieba.lcut(input_str)
    for i in range(0, len(input_words)):
        choice = random.choice([True, False])
        each = input_words[i]
        syn = synonyms.nearby(each)
        if choice and len(syn[1]) > 2:
            if syn[1][1] > 0.7 and each not in syn[0][1]:
                input_str = input_str.replace(each, syn[0][1])
    return input_str


def talk_loop():
    random.seed(time.time())
    hint = '说些什么\n'
    root_path = os.path.dirname(sys.path[0])
    os.chdir(root_path)
    stopwords = 'ChatterBot\\stopwords.txt'
    stopwords_list = open(stopwords, encoding='UTF-8').read().split('\n')
    while True:
        output_str = talk_once(stopwords_list=stopwords_list, hint=hint)
        output_str = syn_replace(output_str)
        print(output_str)
        hint = ''


def talk_once(stopwords_list=None, gi=None, hint=''):
    f_null = open(os.devnull, "w")
    prefix = 'ANY(item IN _.words WHERE item =~ "'
    suffix = '")'
    if gi is None:
        gi = Graph('http://localhost:7474', auth=('neo4j', '20160712'))
    input_str = input(hint)
    words = jieba.lcut(input_str)
    words = list(set(words))
    # remove stopwords
    if stopwords_list is None:
        root_path = os.path.dirname(sys.path[0])
        os.chdir(root_path)
        stopwords = 'ChatterBot\\stopwords.txt'
        stopwords_list = open(stopwords, encoding='UTF-8').read().split('\n')
    if len(words) > 5:
        for each in stopwords_list:
            for word in words:
                if word == each:
                    words.remove(word)
    # query every key words
    results = gi.nodes.match('corpus')
    for word in tqdm(words):
        # TODO : 现在这套检索算法还有很多问题
        # 1.按顺序检索各个词，不能突出不同词的重要性
        # 2.检索深度过深（无关词筛选使意义相近但表示差异大的句子无法被选中）
        # 解决办法 :
        # 1.按词频排序重要性，越少见的词越重要
        # 2.词频大于一定阈值的词不进行检索
        results_temp = results.where(prefix + word + suffix)
        # to prevent over-filtering
        if len(results_temp) < 1:
            pass
        else:
            results = results_temp
    if len(results) > 50:
        return "说详细点，我不知该从何吐槽了"
    score = 0
    candidate_str = None
    if len(results) > 0:
        for i in tqdm(range(0, len(results))):
            # the code in line below spends too much time
            node = results.skip(i).first()
            candidate_reply = gi.match((None, node), r_type='reply')
            if len(candidate_reply) > 0:
                temp = jaccard_similarity(node['content'], input_str)
                # TODO : 相似度计算需要采用新的算法，要更以意近而非形似为重点
                if temp > score:
                    score = temp
                    candidate_str = node
            else:
                pass
        if candidate_str is not None:
            if score < 0.2:
                return "不确定自己有没有理解你所说的。。。欲言又止"
                # the code in above line will be replaced by seq2seq_phrase
            else:
                # print(candidate_str['content'])
                # print('likelihood:'+str(score))
                # print('====================================')
                candidate_reply = gi.match((None, candidate_str), r_type='reply')
                choice = random.randint(0, len(candidate_reply) - 1)
                for each in walk(candidate_reply.skip(choice).first()):
                    if type(each) is Node:
                        if each != candidate_str:
                            print(each, file=f_null)
                            output_str = each['content']
                            # print(output_str)
                return output_str
        else:
            return "别抢我的台词！"
    else:
        return "你说什么？"


def get_node(gi, one_of_pair):
    node = gi.nodes.match('corpus').where(content=one_of_pair).first()
    if node is None:
        node = Node('corpus', content=one_of_pair)
        print(one_of_pair)
        sentiment = SnowNLP(one_of_pair).sentiments
        node['sentiment'] = sentiment
        words = jieba.lcut(one_of_pair)
        words = list(set(words))
        node['words'] = words
    return node


def graph_init(gi=None):
    conversation_pairs, stopwords_list = load_data()
    if gi is None:
        gi = Graph('http://localhost:7474', auth=('neo4j', '20160712'))
    for pair in tqdm(conversation_pairs):
        node_a = get_node(gi=gi, one_of_pair=pair[0])
        node_b = get_node(gi=gi, one_of_pair=pair[1])
        rel = Relationship.type('reply')
        gi.merge(rel(node_b, node_a), 'corpus', "content")


def train():
    root_path = os.path.dirname(sys.path[0])
    os.chdir(root_path)
    train_word.train_start()


def test_seq2seq():
    root_path = os.path.dirname(sys.path[0])
    os.chdir(root_path)
    hint = "测试seq2seq\n"
    while True:
        print(test_model_word.TulpaAvatar(input(hint)))
        hint = ""


# talk_loop()
# train()
# graph_init()
test_seq2seq()

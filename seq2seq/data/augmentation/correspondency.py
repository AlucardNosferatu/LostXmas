import jieba
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.cluster import KMeans
from data.augmentation.frequency import getFreqDist


def getWords(sentence):
    words = []
    for i in range(len(sentence) - 1):
        word = sentence[i] + sentence[i + 1]
        words.append(word)
    return words


def getAllWords(q_lines):
    words_with_dup = []
    for i in tqdm(range(len(q_lines))):
        q = q_lines[i].split('\t')[0].strip()
        a = q_lines[i].split('\t')[1].replace('\n', '').strip()
        words_with_dup += jieba.lcut(q, cut_all=False)
        words_with_dup += jieba.lcut(a, cut_all=False)
    fdist = getFreqDist(words_with_dup)
    return fdist


def sentence2vec(sentence, freq_dist):
    words = jieba.lcut(sentence, cut_all=False)
    if len(words) > 20:
        words = words[:20]
    for i in range(len(words)):
        words[i] = freq_dist.index(words[i])
    while len(words) < 20:
        words.append(len(freq_dist))
    return words


def filterWithCor():
    text_path = "../resource/raw/all_corpus.tsv"
    with open(text_path, 'r+', encoding='utf-8-sig') as f_q:
        q_lines = f_q.readlines()
        fdist = getAllWords(q_lines)
        all_vec = []
        for i in tqdm(range(len(q_lines))):
            try:
                if q_lines[i].startswith('【禁用】'):
                    continue
                q = q_lines[i].split('\t')[0].strip()
                a = q_lines[i].split('\t')[1].replace('\n', '').strip()
                q_vec = sentence2vec(q, fdist)
                a_vec = sentence2vec(a, fdist)
                all_vec.append(q_vec)
                all_vec.append(a_vec)
                q_list = getWords(q)
                a_list = getWords(a)
                inter = list(set(q_list).intersection(set(a_list)))
                if len(inter) == 0:
                    # q_lines[i] = '【禁用】' + q_lines[i]
                    pass
            except Exception as e:
                print(repr(e))
        x = np.array(all_vec)
        y_pred = KMeans(n_clusters=5, random_state=9).fit_predict(x)
        y_pred = list(y_pred)
        q_pred = y_pred[::2]
        a_pred = y_pred[1::2]
        assert len(q_pred) == len(a_pred) == len(q_lines)
        count = 0
        for i in range(len(q_lines)):
            try:
                q = q_lines[i].split('\t')[0].strip()
                a = q_lines[i].split('\t')[1].replace('\n', '').strip()
                if q_pred[i] != a_pred[i]:
                    count += 1
                    print("提问：", q, " 分类：", q_pred[i])
                    print("回答：", a, " 分类：", a_pred[i])
                    print()
            except Exception as e:
                print(repr(e))
        print(count / len(q_lines))
        # f_q.truncate(0)
        # f_q.seek(0)
        # f_q.writelines(q_lines)


if __name__ == '__main__':
    filterWithCor()

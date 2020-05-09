# coding=utf-8
import os
import sys
import nltk
import itertools
import numpy as np
import pickle
from snownlp import SnowNLP
from tqdm import tqdm

EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz '
EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

# 调用文件改为中文对话数据文件
FILENAME = 'seq2seq\\word\\data\\test.txt'

limit = {
    'maxq': 52,
    'minq': 0,
    'maxa': 50,
    'mina': 0
}

UNK = 'unk'
GO = '<go>'
EOS = '<eos>'
PAD = '<pad>'
VOCAB_SIZE = 5000


def read_lines(filename):
    return open(filename, encoding='UTF-8').read().split('\n')


def split_line(line):
    return line.split('.')


def filter_line(line, whitelist):
    return ''.join([ch for ch in line if ch in whitelist])


def index_(tokenized_sentences, vocab_size):
    freq_dist = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    vocab = freq_dist.most_common(vocab_size)
    index2word = [GO] + [EOS] + [UNK] + [PAD] + [x[0] for x in vocab]
    word2index = dict([(w, i) for i, w in enumerate(index2word)])
    return index2word, word2index, freq_dist


def filter_data(sequences):
    filtered_q, filtered_a = [], []
    raw_data_len = len(sequences) // 2
    # 需要注意，两行话为一对话，第一句为问，第二句为答，总行数必须为偶数
    for i in range(0, len(sequences), 2):
        #        q_len, a_len = len(sequences[i].split(' ')), len(sequences[i + 1].split(' '))
        # 使用jieba库进行中文分词
        q_len, a_len = len(sequences[i]), len(sequences[i + 1])
        if limit['minq'] <= q_len <= limit['maxq']:
            if limit['mina'] <= a_len <= limit['maxa']:
                filtered_q.append(sequences[i])
                filtered_a.append(sequences[i + 1])
    filtered_data_len = len(filtered_q)
    filtered = int((raw_data_len - filtered_data_len) * 100 / raw_data_len)
    print(str(filtered) + '% filtered from original data')

    return filtered_q, filtered_a


def zero_pad(q_tokenized, a_tokenized, w2idx):
    data_len = len(q_tokenized)
    # +2 dues to '<go>' and '<eos>'
    idx_q = np.zeros([data_len, limit['maxq']], dtype=np.int32)
    idx_a = np.zeros([data_len, limit['maxa'] + 2], dtype=np.int32)
    idx_o = np.zeros([data_len, limit['maxa'] + 2], dtype=np.int32)

    for i in range(data_len):
        q_indices = pad_seq(q_tokenized[i], w2idx, limit['maxq'], 1)
        a_indices = pad_seq(a_tokenized[i], w2idx, limit['maxa'], 2)
        o_indices = pad_seq(a_tokenized[i], w2idx, limit['maxa'], 3)
        idx_q[i] = np.array(q_indices)
        idx_a[i] = np.array(a_indices)
        idx_o[i] = np.array(o_indices)

    return idx_q, idx_a, idx_o


def pad_seq(seq, lookup, max_len, flag):
    indices = []
    if flag == 1:
        pass
    elif flag == 2:
        indices = [lookup[GO]]
    elif flag == 3:
        pass
    for word in seq:
        if word in lookup:
            indices.append(lookup[word])
        else:
            indices.append(lookup[UNK])
    if flag == 1:
        return indices + [lookup[PAD]] * (max_len - len(seq))
    elif flag == 2:
        return indices + [lookup[EOS]] + [lookup[PAD]] * (max_len - len(seq))
    elif flag == 3:
        return indices + [lookup[EOS]] + [lookup[PAD]] * (max_len - len(seq) + 1)


def remove_duplicate(lines):
    blacklists = get_blacklists(lines)
    whitelist = get_whitelist(blacklists, lines)
    lines = del_redundant(blacklists, whitelist, lines)
    return lines


def del_redundant(blacklists, whitelist, lines):
    blacklists_1d = []
    for blacklist in tqdm(blacklists):
        for each in blacklist:
            blacklists_1d.append(each)
    blacklists_1d.sort()
    whitelist.sort()
    shift = 0
    for each in tqdm(blacklists_1d):
        del (lines[each - shift:each - shift + 2])
        shift += 2
    return lines


def get_whitelist(blacklists, lines):
    whitelist = []
    for blacklist in blacklists:
        highest_score = 0
        highest_index = 0
        print(lines[blacklist[0]])
        for each in tqdm(blacklist):
            score = SnowNLP(lines[each + 1]).sentiments
            if score > highest_score:
                highest_index = each
                highest_score = score
        whitelist.append(highest_index)
    return whitelist


def get_blacklists(lines):
    blacklists = []
    iter_range = list(range(0, len(lines), 2))
    for i in tqdm(iter_range):
        blacklist = [i]
        match_range = iter_range[iter_range.index(i) + 1:len(lines)]
        for j in match_range:
            if lines[i] == lines[j]:
                blacklist.append(j)
                iter_range.remove(j)
        if len(blacklist) >= 2:
            blacklists.append(blacklist)
    # blacklist is a 1d list for storing indices of different instances of one string
    # blacklists is a 2d list for storing blacklists of different strings that duplicated
    return blacklists


def process_data():
    print('\n>> Read lines from file')
    lines = read_lines(filename=FILENAME)
    lines = remove_duplicate(lines)
    #    lines = [line.lower() for line in lines]
    print('\n>> Filter lines')
    #    lines = [filter_line(line, EN_WHITELIST) for line in lines]
    # 取消英文字符白名单过滤
    print('\n>> 2nd layer of filtering')
    q_lines, a_lines = filter_data(lines)

    print('\n>> Segment lines into words')
    # 使用list将字符串直接分解成字的列表
    q_tokenized = [list(word_list) for word_list in q_lines]
    a_tokenized = [list(word_list) for word_list in a_lines]

    print('\n>> Index words')
    idx2w, w2idx, freq_dist = index_(q_tokenized + a_tokenized, vocab_size=VOCAB_SIZE)
    with open('seq2seq\\word\\idx2w.pkl', 'wb') as f:
        pickle.dump(idx2w, f)
    with open('seq2seq\\word\\w2idx.pkl', 'wb') as f:
        pickle.dump(w2idx, f)
    idx_q, idx_a, idx_o = zero_pad(q_tokenized, a_tokenized, w2idx)

    print('\n>> Save numpy arrays to disk')
    np.save('seq2seq\\word\\idx_q_word.npy', idx_q)
    np.save('seq2seq\\word\\idx_a_word.npy', idx_a)
    np.save('seq2seq\\word\\idx_o_word.npy', idx_o)

    metadata = {
        'w2idx': w2idx,
        'idx2w': idx2w,
        'limit': limit,
        'freq_dist': freq_dist
    }

    with open('seq2seq\\word\\metadata_w.pkl', 'wb') as f:
        pickle.dump(metadata, f)


def load_data(path=''):
    with open(path + 'metadata_w.pkl', 'rb') as f:
        metadata = pickle.load(f)
    idx_q = np.load(path + 'idx_q_word.npy')
    idx_a = np.load(path + 'idx_a_word.npy')
    return metadata, idx_q, idx_a


if __name__ == '__main__':
    rootPath = os.path.dirname(os.path.dirname(sys.path[0]))
    os.chdir(rootPath)
    process_data()

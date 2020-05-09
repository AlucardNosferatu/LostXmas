# coding=utf-8
import os
import sys
import nltk
import itertools
import numpy as np
import pickle
import jieba
from tqdm import tqdm
from snownlp import SnowNLP

EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz '
EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

# 调用文件改为中文对话数据文件
FILENAME = 'RASA_data\\nlu.md'

limit = {
    'maxq': 32,
    'minq': 0,
    'maxa': 30,
    'mina': 0
}

UNK = 'unk'
GO = '<go>'
EOS = '<eos>'
PAD = '<pad>'
VOCAB_SIZE = 300000


def read_lines(filename):
    return open(filename, encoding='UTF-8-sig').read().split('\n')


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
    mark = ""
    data = []
    data_mark = []
    for i in range(0, len(sequences)):
        if "## intent" in sequences[i]:
            mark = sequences[i].lstrip("## intent:").strip("\n")
        elif sequences[i] == "":
            mark_copy = data_mark.copy()
            data.append([mark, mark_copy])
            mark = ""
            data_mark.clear()
        elif "- " in sequences[i]:
            temp = sequences[i].lstrip("- ").strip("\n")
            temp = jieba.lcut(temp)
            # this is for English space
            while " " in temp:
                temp.remove(" ")
            data_mark.append(temp)
        else:
            pass
    return data


def zero_pad(sequences, w2idx):
    data_len = len(sequences)
    # +2 dues to '<go>' and '<eos>'
    idx_q = np.zeros([data_len, limit['maxq']], dtype=np.int32)
    for i in range(data_len):
        q_indices = pad_seq(sequences[i], w2idx, limit['maxq'], 1)
        idx_q[i] = np.array(q_indices)
    return idx_q


def pad_seq(seq, lookup, maxlen, flag):
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
        return indices + [lookup[PAD]] * (maxlen - len(seq))
    elif flag == 2:
        return indices + [lookup[EOS]] + [lookup[PAD]] * (maxlen - len(seq))
    elif flag == 3:
        return indices + [lookup[EOS]] + [lookup[PAD]] * (maxlen - len(seq) + 1)


def process_data():
    print('\n>> Read lines from file')
    lines = read_lines(filename=FILENAME)
    data = filter_data(lines)
    data_mix = []
    for data_mark in data:
        data_mix += data_mark[1]
    idx2w, w2idx, freq_dist = index_(data_mix, vocab_size=VOCAB_SIZE)
    with open('RASA_data\\idx2p.pkl', 'wb') as f:
        pickle.dump(idx2w, f)
    with open('RASA_data\\p2idx.pkl', 'wb') as f:
        pickle.dump(w2idx, f)
    temp = []
    for data_mark in data:
        data_padded = zero_pad(data_mark[1], w2idx)
        temp.append([data_mark[0], data_padded])
        np.save("RASA_data\\"+data_mark[0]+'.npy', data_padded)

    metadata = {
        'p2idx': w2idx,
        'idx2p': idx2w,
        'limit': limit,
        'freq_dist': freq_dist
    }

    with open('RASA_data\\metadata_p.pkl', 'wb') as f:
        pickle.dump(metadata, f)


if __name__ == '__main__':
    process_data()

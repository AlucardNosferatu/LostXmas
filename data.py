import pickle
import random

import jieba
import torch
from torch.utils.data import Dataset


class PairDataset(Dataset):
    def __init__(self, data_pairs, max_len=128, pad_id=0):
        self.pairs = data_pairs
        self.max_len = max_len
        self.pad_id = pad_id

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        # 对数据对进行填充/截断处理，确保长度不超过max_length
        # 使用pad_id填充不足部分，保证批次内序列长度对齐 [[4]]
        src, tgt = self.pairs[idx]
        # 添加填充和截断
        src = self._pad_sequence(src)
        tgt = self._pad_sequence(tgt)
        return torch.LongTensor(src), torch.LongTensor(tgt)

    def _pad_sequence(self, sequence):
        truncated = sequence[:self.max_len]  # 截断
        padded = truncated + [self.pad_id] * (self.max_len - len(truncated))  # 填充
        return torch.LongTensor(padded)


class ConcatShiftedDataset(Dataset):
    def __init__(self, data_concat, max_len=128, pad_id=0, sos_id=1):
        self.data_concat = data_concat
        self.max_len = max_len
        self.pad_id = pad_id
        self.sos_id = sos_id

    def __len__(self):
        return len(self.data_concat)

    def __getitem__(self, idx):
        # 对数据对进行填充/截断处理，确保长度不超过max_length
        # 使用pad_id填充不足部分，保证批次内序列长度对齐 [[4]]
        tgt = self.data_concat[idx]
        tgt_shifted = tgt.copy()
        tgt_shifted.pop(0)
        # 添加填充和截断
        tgt = self._pad_sequence(tgt)
        tgt_shifted = self._pad_sequence(tgt_shifted)
        return tgt, tgt_shifted

    def _pad_sequence(self, sequence):
        truncated = sequence[:self.max_len]  # 截断
        padded = truncated + [self.pad_id] * (self.max_len - len(truncated))  # 填充
        return torch.LongTensor(padded)


class ConcatTruncatedDataset(Dataset):
    def __init__(self, data_concat, max_len=128, pad_id=0, sos_id=1, eos_id=2):
        self.data_concat = data_concat
        self.max_len = max_len
        self.pad_id = pad_id
        self.sos_id = sos_id
        self.eos_id = eos_id

    def __len__(self):
        return len(self.data_concat)

    def __getitem__(self, idx):
        # 对数据对进行填充/截断处理，确保长度不超过max_length
        # 使用pad_id填充不足部分，保证批次内序列长度对齐 [[4]]
        tgt = self.data_concat[idx]
        tgt_len, first_eos = tgt[1], tgt[2]
        tgt = tgt[0].copy()
        truncate_after = random.randint(first_eos + 1, tgt_len - 1)
        tgt_next_token = torch.LongTensor([tgt[truncate_after]])
        tgt[truncate_after:] = [self.pad_id] * (len(tgt) - truncate_after)
        tgt = self._pad_sequence(tgt)
        return tgt, tgt_next_token

    def _pad_sequence(self, sequence):
        truncated = sequence[:self.max_len]  # 截断
        padded = truncated + [self.pad_id] * (self.max_len - len(truncated))  # 填充
        return torch.LongTensor(padded)


def get_vocab(lines_words, new_vocab, tag_fill_this=False):
    if new_vocab:
        words_count = {}
        for line_words in lines_words:
            for word in line_words:
                if word not in words_count.keys():
                    words_count[word] = 0
                words_count[word] += 1
        words_count_sorted = sorted(words_count, key=lambda x: words_count[x], reverse=True)
        if '[PAD]' not in words_count_sorted:
            words_count_sorted.insert(0, '[PAD]')
        if '[SOS]' not in words_count_sorted:
            words_count_sorted.insert(0, '[SOS]')
        if '[EOS]' not in words_count_sorted:
            words_count_sorted.insert(0, '[EOS]')
        words_count_sorted.insert(0, '[UNK]')
        if tag_fill_this:
            words_count_sorted.insert(0, '[FTB]')  # FTB for "fill this blank"
        with open(file='data/vocab.pkl', mode='wb') as f:
            pickle.dump(obj=words_count_sorted, file=f)
    else:
        with open(file='data/vocab.pkl', mode='rb') as f:
            words_count_sorted = pickle.load(file=f)
    return words_count_sorted


def read_corpus(filepath='conv.txt', pad_now=True, add_sos=True, add_eos=True):
    with open(file=filepath, mode='r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if len(line.strip()) > 0]
    lines_words = [jieba.lcut(line) for line in lines]
    if add_sos:
        lines_words = [['[SOS]'] + line_words for line_words in lines_words]
    if add_eos:
        lines_words = [line_words + ['[EOS]'] for line_words in lines_words]
    max_length = max([len(line_words) for line_words in lines_words])
    if pad_now:
        for line_words in lines_words:
            while len(line_words) < max_length:
                line_words.append('[PAD]')
    return lines_words, max_length


def tokenize(lines_words, words_list):
    lines_ids = []
    for line_words in lines_words:
        line_ids = []
        for word in line_words:
            if word in words_list:
                line_ids.append(words_list.index(word))
            else:
                line_ids.append(words_list.index('[UNK]'))
        lines_ids.append(line_ids.copy())
    return lines_ids


def sentence_to_tensor(sentence, words_list, max_length):
    sentence_words_list = [jieba.lcut(sentence)]
    sentence_ids_list = tokenize(lines_words=sentence_words_list, words_list=words_list)[0]
    sentence_ids_list.insert(0, words_list.index('[SOS]'))  # 假设存在词汇表对象
    sentence_ids_list.append(words_list.index('[EOS]'))

    while len(sentence_ids_list) < max_length:
        sentence_ids_list.append(words_list.index('[PAD]'))
    # 假设存在词汇表对象
    sentence_tensor = torch.tensor(sentence_ids_list).unsqueeze(0)  # 添加batch维度[[1]]
    return sentence_tensor

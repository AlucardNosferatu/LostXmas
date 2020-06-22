import pickle
import jieba
import numpy as np
from tqdm import tqdm
from tensorflow.keras.preprocessing import sequence

from data.data_tool import Traditional2Simplified, is_all_chinese, is_pure_english


def read_conv():
    # region get Q&A
    with open('resource/raw/qingyun.tsv', 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        lines = lines[:-2]
    question = []
    answer = []
    for pos, line in enumerate(tqdm(lines)):
        if '\t' not in line:
            print(line)
        line = line.split('\t')
        q = line[0].strip()
        a = line[1].strip()
        question.append(' '.join(jieba.lcut(Traditional2Simplified(q).strip(), cut_all=False)))
        answer.append(' '.join(jieba.lcut(Traditional2Simplified(a).strip(), cut_all=False)))
    with open('resource/raw/legacy/question.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for pos, line in enumerate(tqdm(lines)):
            question.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    with open('resource/raw/legacy/answer.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for pos, line in enumerate(tqdm(lines)):
            answer.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    # endregion

    character = set()
    for seq in tqdm(question + answer):
        word_list = seq.split(' ')
        for word in word_list:
            if not is_all_chinese(word):
                character.add(word)
    character = list(character)
    stop_words = set()
    for pos, word in enumerate(tqdm(character)):
        if not is_pure_english(word):
            stop_words.add(word)
    maxLen = 18
    for pos, seq in enumerate(tqdm(question)):
        seq_list = seq.split(' ')
        for epoch in range(3):
            for pos_, word in enumerate(seq_list):
                if word in stop_words:
                    seq_list.pop(pos_)
        if len(seq_list) > maxLen:
            seq_list = seq_list[:maxLen]
        question[pos] = ' '.join(seq_list)
    for pos, seq in enumerate(tqdm(answer)):
        seq_list = seq.split(' ')
        for epoch in range(3):
            for pos_, word in enumerate(seq_list):
                if word in stop_words:
                    seq_list.pop(pos_)
        if len(seq_list) > maxLen:
            seq_list = seq_list[:maxLen]
        answer[pos] = ' '.join(seq_list)
    answer_a = ['BOS ' + i + ' EOS' for i in answer]
    answer_b = [i + ' EOS' for i in answer]
    counts = {}
    BE = ['BOS', 'EOS']
    for word_list in tqdm(question + answer + BE):
        for word in word_list.split(' '):
            counts[word] = counts.get(word, 0) + 1
    word_to_index = {}
    for pos, i in enumerate(tqdm(counts.keys())):
        word_to_index[i] = pos
    index_to_word = {}
    for pos, i in enumerate(tqdm(counts.keys())):
        index_to_word[pos] = i
    vocab_bag = list(word_to_index.keys())
    with open('resource/word_to_index.pkl', 'wb') as f:
        pickle.dump(word_to_index, f, pickle.HIGHEST_PROTOCOL)
    with open('resource/index_to_word.pkl', 'wb') as f:
        pickle.dump(index_to_word, f, pickle.HIGHEST_PROTOCOL)
    with open('resource/vocab_bag.pkl', 'wb') as f:
        pickle.dump(vocab_bag, f, pickle.HIGHEST_PROTOCOL)
    question = np.array([[word_to_index[w] for w in i.split(' ')] for i in question])
    answer_a = np.array([[word_to_index[w] for w in i.split(' ')] for i in answer_a])
    answer_b = np.array([[word_to_index[w] for w in i.split(' ')] for i in answer_b])
    np.save('resource/question.npy', question[:100000])
    np.save('resource/answer_a.npy', answer_a[:100000])
    np.save('resource/answer_b.npy', answer_b[:100000])


def add_padding():
    question = np.load('resource/question.npy', allow_pickle=True)
    answer_a = np.load('resource/answer_a.npy', allow_pickle=True)
    answer_b = np.load('resource/answer_b.npy', allow_pickle=True)
    print('answer_a.shape: ', answer_a.shape)
    with open('resource/word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    for i, j in tqdm(word_to_index.items()):
        word_to_index[i] = j + 1
    index_to_word = {}
    for key, value in tqdm(word_to_index.items()):
        index_to_word[value] = key
    pad_question = question
    pad_answer_a = answer_a
    pad_answer_b = answer_b
    maxLen = 20
    for pos, i in enumerate(tqdm(pad_question)):
        for pos_, j in enumerate(i):
            i[pos_] = j + 1
        if len(i) > maxLen:
            pad_question[pos] = i[:maxLen]
    for pos, i in enumerate(tqdm(pad_answer_a)):
        for pos_, j in enumerate(i):
            i[pos_] = j + 1
        if len(i) > maxLen:
            pad_answer_a[pos] = i[:maxLen]
    for pos, i in enumerate(tqdm(pad_answer_b)):
        for pos_, j in enumerate(i):
            i[pos_] = j + 1
        if len(i) > maxLen:
            pad_answer_b[pos] = i[:maxLen]
    np.save('resource/answer_o.npy', pad_answer_b)
    with open('resource/vocab_bag.pkl', 'rb') as f:
        words = pickle.load(f)
    vocab_size = len(word_to_index) + 1
    print('word_to_vec_map: ', len(list(words)))
    print('vocab_size: ', vocab_size)
    pad_question = sequence.pad_sequences(pad_question, maxlen=maxLen,
                                          dtype='int32', padding='post',
                                          truncating='post')
    pad_answer = sequence.pad_sequences(pad_answer_a, maxlen=maxLen,
                                        dtype='int32', padding='post',
                                        truncating='post')
    with open('resource/pad_word_to_index.pkl', 'wb') as f:
        pickle.dump(word_to_index, f, pickle.HIGHEST_PROTOCOL)
    with open('resource/pad_index_to_word.pkl', 'wb') as f:
        pickle.dump(index_to_word, f, pickle.HIGHEST_PROTOCOL)
    np.save('resource/pad_question.npy', pad_question)
    np.save('resource/pad_answer.npy', pad_answer)


if __name__ == '__main__':
    # read_conv()
    add_padding()

import pickle

import jieba
import numpy as np
from tensorflow.keras.preprocessing import sequence
from tqdm import tqdm

from data.augmentation.blacklist import DFAFilter
from data.augmentation.compressor import getSynDict
from data.augmentation.decomposition import getBaseWord, getComposed
from data.augmentation.frequency import getWords
from data.data_tool import Traditional2Simplified, is_all_chinese, is_pure_english, remove_brackets, append_extra_data, \
    remove_banned


def read_conversation(forceSyn=True):
    # region get Q&A
    gfw = DFAFilter()
    gfw.parse('augmentation\\blacklist')
    with open('resource/raw/all_corpus.tsv', 'r', encoding='utf-8-sig') as f:
        lines = f.read().split('\n')
        lines = lines[:-2]
        lines = remove_brackets(lines)
        lines = remove_banned(lines)
    question = []
    answer = []
    for i in tqdm(range(len(lines))):
        line = lines[i]
        if '\t' not in line:
            print(line)
        line = line.split('\t')
        q = line[0].strip()
        a = line[1].strip()
        q_filter = gfw.filter(q, '*')
        a_filter = gfw.filter(a, '*')
        if q_filter[1] or a_filter[1]:
            # print(q_filter[0])
            # print(a_filter[0])
            continue
        question.append(' '.join(jieba.lcut(Traditional2Simplified(q).strip(), cut_all=False)))
        answer.append(' '.join(jieba.lcut(Traditional2Simplified(a).strip(), cut_all=False)))
    # endregion

    # region Append extra data
    # question, answer = getExtra(gfw, question, answer)
    # endregion

    # region Append test log
    q_path = '../infer/Online_Q.txt'
    a_path = '../infer/Online_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    # endregion

    # region Process special chars
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
    # endregion

    # region Process questions
    for pos, seq in enumerate(tqdm(question)):
        seq_list = seq.split(' ')
        for epoch in range(3):
            for pos_, word in enumerate(seq_list):
                if word in stop_words:
                    seq_list.pop(pos_)
        if len(seq_list) > maxLen:
            seq_list = seq_list[:maxLen]
        question[pos] = ' '.join(seq_list)
    # endregion

    # region Process answers
    for pos, seq in enumerate(tqdm(answer)):
        seq_list = seq.split(' ')
        for epoch in range(3):
            for pos_, word in enumerate(seq_list):
                if word in stop_words:
                    seq_list.pop(pos_)
        if len(seq_list) > maxLen:
            seq_list = seq_list[:maxLen]
        answer[pos] = ' '.join(seq_list)
    # endregion

    # region Compress synonyms
    _, freq_dist = getWords(question + answer)
    syn_dict = getSynDict(freq_dist)
    with open('resource/' + 'syn_dict.pkl', 'wb') as f:
        pickle.dump(syn_dict, f, pickle.HIGHEST_PROTOCOL)
    if forceSyn:
        sentences = [question, answer]
        for i in range(len(sentences)):
            sentence = sentences[i]
            for j in tqdm(range(len(sentence))):
                words = sentence[j].split(' ')
                for k in range(len(words)):
                    for key in syn_dict:
                        if words[k] in syn_dict[key] and len(words[k]) >= 2:
                            words[k] = key
                            break
                sentence[j] = ' '.join(words)
            sentences[i] = sentence
        question, answer = sentences
    # endregion

    # region Decompose phrases
    _, freq_dist = getWords(question + answer)
    base_words = getBaseWord(freq_dist)
    all_composable = getComposed(base_words, freq_dist)
    with open('resource/composable.pkl', 'wb') as f:
        pickle.dump(all_composable, f, pickle.HIGHEST_PROTOCOL)
    for comp in all_composable:
        del freq_dist[freq_dist.index(comp)]
    sentences = [question, answer]
    for i in range(len(sentences)):
        sentence = sentences[i]
        for j in tqdm(range(len(sentence))):
            words = sentence[j].split(' ')
            for k in range(len(words)):
                if words[k] in all_composable:
                    words[k] = ' '.join(list(words[k]))
            sentence[j] = ' '.join(words)
        sentences[i] = sentence
    question, answer = sentences
    # endregion

    placeholders = ['BOS', 'EOS']
    _, freq_dist = getWords(question + answer + placeholders)
    word_to_index = {}
    for pos, i in enumerate(tqdm(freq_dist)):
        word_to_index[i] = pos
    index_to_word = {}
    for pos, i in enumerate(tqdm(freq_dist)):
        index_to_word[pos] = i
    vocab_bag = list(word_to_index.keys())

    answer_a = ['BOS ' + i + ' EOS' for i in answer]
    answer_b = [i + ' EOS' for i in answer]
    with open('resource/word_to_index.pkl', 'wb') as f:
        pickle.dump(word_to_index, f, pickle.HIGHEST_PROTOCOL)
    with open('resource/index_to_word.pkl', 'wb') as f:
        pickle.dump(index_to_word, f, pickle.HIGHEST_PROTOCOL)
    with open('resource/vocab_bag.pkl', 'wb') as f:
        pickle.dump(vocab_bag, f, pickle.HIGHEST_PROTOCOL)
    question = np.array([[word_to_index[w] for w in i.split(' ')] for i in question])
    answer_a = np.array([[word_to_index[w] for w in i.split(' ')] for i in answer_a])
    answer_b = np.array([[word_to_index[w] for w in i.split(' ')] for i in answer_b])
    size = int(len(question) / 100) * 100
    np.save('resource/question.npy', question[:size])
    np.save('resource/answer_a.npy', answer_a[:size])
    np.save('resource/answer_b.npy', answer_b[:size])


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


def getExtra(gfw, question, answer):
    q_path = 'obsolete/legacy/compact_vocab_Q.txt'
    a_path = 'obsolete/legacy/compact_vocab_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/CPoL4OC_Q.txt'
    a_path = 'obsolete/legacy/CPoL4OC_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/Lovers_Q.txt'
    a_path = 'obsolete/legacy/Lovers_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/MyTulpa_Q.txt'
    a_path = 'obsolete/legacy/MyTulpa_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/XiaoIce_Q.txt'
    a_path = 'obsolete/legacy/XiaoIce_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/YellowChick_Q.txt'
    a_path = 'obsolete/legacy/YellowChick_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'obsolete/legacy/ChatterBot_Q.txt'
    a_path = 'obsolete/legacy/ChatterBot_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    return question, answer


if __name__ == '__main__':
    read_conversation()
    add_padding()

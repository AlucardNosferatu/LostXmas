import pickle

import numpy as np


def get_vocab_size():
    main_path = '../data/'
    with open(main_path + 'resource/' + 'pad_word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    vocab_size = len(word_to_index) + 1
    return vocab_size


def generate_train(batch_size):
    main_path = '../data/'
    question = np.load(main_path + 'resource/' + 'pad_question.npy')
    answer = np.load(main_path + 'resource/' + 'pad_answer.npy')
    answer_o = np.load(main_path + 'resource/' + 'answer_o.npy', allow_pickle=True)
    with open(main_path + 'resource/' + 'vocab_bag.pkl', 'rb') as f:
        words = pickle.load(f)
    with open(main_path + 'resource/' + 'pad_word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    with open(main_path + 'resource/' + 'pad_index_to_word.pkl', 'rb') as f:
        index_to_word = pickle.load(f)
    vocab_size = len(word_to_index) + 1
    maxLen = 20
    print('\n*********************************generate_train()*********************************')
    steps = 0
    question_ = question
    answer_ = answer
    while True:
        batch_answer_o = answer_o[steps:steps + batch_size]
        batch_question = question_[steps:steps + batch_size]
        batch_answer = answer_[steps:steps + batch_size]
        outs = np.zeros([batch_size, maxLen, vocab_size], dtype='float32')
        for pos, i in enumerate(batch_answer_o):
            for pos_, j in enumerate(i):
                if pos_ > 20:
                    print(i)
                outs[pos, pos_, j] = 1  # one-hot
        yield [batch_question, batch_answer], outs
        steps += batch_size
        if steps == 100000:
            steps = 0

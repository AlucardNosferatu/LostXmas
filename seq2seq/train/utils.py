import pickle

import numpy as np

from w2v.w2v_test import init_w2v


def get_vocab_size(base_dir='../'):
    main_path = base_dir + 'data/'
    with open(main_path + 'resource/' + 'pad_word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    vocab_size = len(word_to_index) + 1
    return vocab_size


def load_resource(base_dir='../'):
    main_path = base_dir + 'data/'
    question = np.load(main_path + 'resource/' + 'pad_question.npy')
    answer = np.load(main_path + 'resource/' + 'pad_answer.npy')
    answer_o = np.load(main_path + 'resource/' + 'answer_o.npy', allow_pickle=True)
    with open(main_path + 'resource/' + 'vocab_bag.pkl', 'rb') as f:
        words = pickle.load(f)
    with open(main_path + 'resource/' + 'pad_word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    with open(main_path + 'resource/' + 'pad_index_to_word.pkl', 'rb') as f:
        index_to_word = pickle.load(f)
    return question, answer, answer_o, words, word_to_index, index_to_word


def generate_train(batch_size, base_dir="../", use_w2v=True):
    question, answer, answer_o, _, word_to_index, _ = load_resource(base_dir=base_dir)
    if use_w2v:
        w2v = init_w2v()
        vocab_size = len(w2v.index2word)
    else:
        vocab_size = len(word_to_index) + 1
    max_len = 20
    print('\n*********************************generate_train()*********************************')
    steps = 0
    question_ = question
    answer_ = answer
    yield int(len(question) / batch_size)
    while True:
        batch_answer_o = answer_o[steps:steps + batch_size]
        batch_question = question_[steps:steps + batch_size]
        batch_answer = answer_[steps:steps + batch_size]
        outs = np.zeros([batch_size, max_len, vocab_size], dtype='float32')
        for pos, i in enumerate(batch_answer_o):
            for pos_, j in enumerate(i):
                if pos_ > 20:
                    print(i)
                outs[pos, pos_, j] = 1  # one-hot
        yield [batch_question, batch_answer], outs
        # print(steps)
        steps += batch_size
        if steps == len(question):
            steps = 0
            state = np.random.get_state()
            np.random.shuffle(answer_o)
            np.random.set_state(state)
            np.random.shuffle(question_)
            np.random.set_state(state)
            np.random.shuffle(answer_)

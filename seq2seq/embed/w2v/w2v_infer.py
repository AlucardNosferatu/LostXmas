import jieba
import numpy as np
from tensorflow.keras.preprocessing import sequence

from infer.utils import maxLen
from server.hyper_transformer import recursive_translator
from embed.w2v.w2v_emb_test import init_w2v


def input_question_w2v(seq, w2v=None):
    use_syn = False
    if w2v is None:
        w2v = init_w2v()
    seq = seq.replace('，', ',').replace('。', '.')
    seq = jieba.lcut(seq.strip(), cut_all=False)
    word_to_index = list(w2v.vocab.keys())
    for k in range(len(seq)):
        if not seq[k] in w2v.vocab:
            use_syn = True
            seq[k] = recursive_translator(word_to_index, seq[k], 0)
            # seq[k] = translator(word_to_index, seq[k])
            # seq[k] = w2v.most word_to_index, seq[k], 0)
    seq = ' '.join(seq)
    if use_syn:
        print("出现未知词汇，采用同义词替换：")
        print(seq.replace(' ', ''))
    seq = seq.split(' ')
    try:
        seq = np.array([w2v.vocab[w].index for w in seq])
        seq = sequence.pad_sequences([seq], maxlen=maxLen,
                                     padding='post', truncating='post', value=w2v.vocab['PAD'].index)
    except KeyError as e:
        seq = "出现了Carol没法理解的词汇。。。：" + str(e.args[0])
        print(seq)
    return seq


def decode_greedy_w2v(seq, question_model, answer_model, word2vec):
    question = seq
    answer = np.zeros((1, 1))
    answer[0, 0] = word2vec.vocab['BOS'].index

    i = 1
    answer_ = []
    flag = 0
    encoder_lstm_, question_h, question_c = question_model.predict(x=question, verbose=1)
    while flag != 1:
        prediction, prediction_h, prediction_c, _ = answer_model.predict([
            answer, question_h, question_c, encoder_lstm_
        ])
        word_arg = np.argmax(prediction[0, -1, :])  #
        answer_.append(word2vec.index2word[word_arg])
        if word_arg == word2vec.vocab['EOS'].index or i > 20:
            flag = 1
        answer = np.zeros((1, 1))
        answer[0, 0] = word_arg
        question_h = prediction_h
        question_c = prediction_c
        i += 1

    return ''.join(answer_).replace('EOS', '')


if __name__ == '__main__':
    input_question_w2v(seq="回见")

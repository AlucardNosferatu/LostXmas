import jieba
import matplotlib
import matplotlib.pyplot as plt
import requests
import numpy as np
import synonyms
from tensorflow.keras.preprocessing import sequence

from server.hyper_transformer import translator, recursive_translator
from w2v.w2v_test import word2vector

maxLen = 20


def act_weather(city):
    # TODO: Get weather by api
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
    page = requests.get(url)
    data = page.json()
    temperature = data['data']['wendu']
    notice = data['data']['ganmao']
    outstrs = "地点： %s\n气温： %s\n注意： %s" % (city, temperature, notice)
    return outstrs + ' EOS'


def input_question(seq, word_to_index, embed="word2vec"):
    seq = seq.replace('，', ',').replace('。', '.')
    seq = jieba.lcut(seq.strip(), cut_all=False)
    use_syn = False
    if embed == "word2vec":
        for k in range(len(seq)):
            if not seq[k] in word_to_index.wv.vocab:
                use_syn = True
                seq[k] = recursive_translator(word_to_index.wv.vocab, seq[k], 0)
        seq = ' '.join(seq)
        if use_syn:
            print("出现未知词汇，采用同义词替换：")
            print(seq.replace(' ', ''))
        seq = seq.split(' ')
        try:
            seq = np.array([word_to_index.wv.word_vec(w, use_norm=True) for w in seq])
            seq = sequence.pad_sequences(
                [seq],
                maxlen=maxLen,
                dtype='float32',
                padding='post',
                truncating='post'
            )
        except KeyError as e:
            seq = "出现了Carol没法理解的词汇。。。：" + str(e.args[0])
            print(seq)
    else:
        for k in range(len(seq)):
            if not seq[k] in word_to_index:
                use_syn = True
                # seq[k] = translator(word_to_index, seq[k])
                seq[k] = recursive_translator(word_to_index, seq[k], 0)
        seq = ' '.join(seq)
        if use_syn:
            print("出现未知词汇，采用同义词替换：")
            print(seq.replace(' ', ''))
        seq = seq.split(' ')
        try:
            seq = np.array([word_to_index[w] for w in seq])
            seq = sequence.pad_sequences([seq], maxlen=maxLen,
                                         padding='post', truncating='post')
        except KeyError as e:
            seq = "出现了Carol没法理解的词汇。。。：" + str(e.args[0])
            print(seq)
    return seq


def decode_greedy(seq, question_model, answer_model, word_to_index, index_to_word, embed="word2vec"):
    question = seq
    if embed == 'word2vec':
        answer = np.zeros((1, 50))
    else:
        answer = np.zeros((1, 1))
    attention_plot = np.zeros((20, 20))
    if embed == "word2vec":
        answer[0, :] = word_to_index.wv.word_vec('BOS', use_norm=True)
    else:
        answer[0, 0] = word_to_index['BOS']

    i = 1
    answer_ = []
    flag = 0
    encoder_lstm_, question_h, question_c = question_model.predict(x=question, verbose=1)
    #     print(question_h, '\n')
    while flag != 1:
        prediction, prediction_h, prediction_c, attention = answer_model.predict([
            answer, question_h, question_c, encoder_lstm_
        ])
        attention_weights = attention.reshape(-1, )
        attention_plot[i] = attention_weights
        word_arg = np.argmax(prediction[0, -1, :])  #
        answer_.append(index_to_word[word_arg])
        if word_arg == word_to_index['EOS'] or i > 20:
            flag = 1
        answer = np.zeros((1, 1))
        answer[0, 0] = word_arg
        question_h = prediction_h
        question_c = prediction_c
        i += 1

    return ''.join(answer_).replace('EOS', '')


def decode_beamsearch(seq, beam_size, question_model, answer_model, word_to_index, index_to_word):
    question = seq
    encoder_lstm_, question_h, question_c = question_model.predict(x=question, verbose=1)
    sequences = [[[word_to_index['BOS']], 1.0, question_h, question_c]]
    answer = np.zeros((1, 1))
    answer[0, 0] = word_to_index['BOS']
    answer_ = ''
    flag = 0
    last_words = [word_to_index['BOS']]
    for i in range(maxLen):
        all_candidates = []
        for j in range(len(sequences)):
            s, score, h, c = sequences[j]
            last_word = s[-1]
            if not isinstance(last_word, int):
                last_word = last_word[-1]
            answer[0, 0] = last_word
            output, h, c, _ = answer_model.predict([answer, h, c, encoder_lstm_])
            output = output[0, -1]
            for k in range(len(output)):
                candidate = [seq + [k], score * -np.log(output[k]), h, c]
            all_candidates.append(candidate)
        ordered = sorted(all_candidates, key=lambda tup: tup[1])
        sequences = ordered[:beam_size]
    answer_ = sequences[0][0]
    print(answer_[0])
    answer_ = [index_to_word[x] for x in answer_[0] if (x != 0)]
    answer_ = ' '.join(answer_)
    return answer_


def plot_attention(attention, sentence, predicted_sentence):
    zhfont = matplotlib.font_manager.FontProperties(fname='simkai.ttf')
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    attention = [x[::-1] for x in attention]
    ax.matshow(attention, cmap='viridis')
    fontdict = {'fontsize': 20}
    ax.set_xticklabels([''] + sentence, fontdict=fontdict, fontproperties=zhfont)
    ax.set_yticklabels([''] + predicted_sentence, fontdict=fontdict, fontproperties=zhfont)
    #     ax.yaxis.set_ticks_position('right') #y轴刻度位置靠右
    plt.show()

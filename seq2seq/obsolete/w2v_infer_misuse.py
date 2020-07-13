import jieba
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from tensorflow.keras.preprocessing import sequence
from obsolete.grammar4fluency import mark_invalid
from data.augmentation.similarity import similarity_complex, Keywords_IoU
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, dot, Activation, concatenate
from obsolete.w2v_train_misuse import build_seq2seq
from server.hyper_transformer import recursive_translator
from train.utils import get_vocab_size, load_resource
from embed.w2v.w2v_emb_test import init_w2v

maxLen = 20


def decode_greedy(seq, question_model, answer_model, word_to_index, index_to_word, embed="word2vec"):
    question = seq
    if embed == 'word2vec':
        answer = np.zeros((1, 1, 50))
    else:
        answer = np.zeros((1, 1))
    attention_plot = np.zeros((20, 20))
    if embed == "word2vec":
        answer[0, 0, :] = word_to_index.wv.word_vec('BOS', use_norm=True)
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
        if embed == "word2vec":
            word_arg = np.squeeze(prediction)
            word = word_to_index.most_similar(positive=[word_arg], topn=1)[0][0]
            answer_.append(word)
            if word == "EOS" or i > 20:
                flag = 1
            answer = prediction
        else:
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


def build_qa_model(base_dir, wp=None, embed="word2vec"):
    max_len = 20
    iq, el, qh, qc, ld, iae, dd1, dd2, ia = build_seq2seq(
        base_dir=base_dir,
        vocab_size=get_vocab_size(base_dir=base_dir),
        weight_path=wp,
        embed=embed
    )
    question_model = Model(iq, [el, qh, qc])
    question_model.summary()

    answer_h = Input(shape=(512,))
    answer_c = Input(shape=(512,))

    el = Input(shape=(max_len, 512))

    target, h, c = ld(iae, initial_state=[answer_h, answer_c])
    attention = dot([target, el], axes=[2, 2])
    attention_ = Activation('softmax')(attention)
    context = dot([attention_, el], axes=[2, 1])
    decoder_combined_context = concatenate([context, target])
    output = dd1(decoder_combined_context)  # equation (5) of the paper
    output = dd2(output)  # equation (6) of the paper
    answer_model = Model([ia, answer_h, answer_c, el], [output, h, c, attention_])
    answer_model.summary()
    return question_model, answer_model


def loop_talking(use_keywords=False, base_dir='../', embed="word2vec"):
    f_r = open(base_dir + "data/resource/raw/all_corpus.tsv", 'r+', encoding='utf-8-sig')
    raw_lines = f_r.readlines()
    lines = raw_lines.copy()
    for i in tqdm(range(len(raw_lines))):
        raw_lines[i] = raw_lines[i].split('\t')[1].replace('\n', '').strip()
    all_lines = [raw_lines]
    question_model, answer_model = build_qa_model(
        base_dir=base_dir,
        wp=base_dir + "train/check_points/W -  1-0.0006-.h5"
    )
    _, _, _, _, word_to_index, index_to_word = load_resource(base_dir=base_dir)
    if embed == "word2vec":
        word_to_index = init_w2v()

    f_q = open(base_dir + "infer/Online_Q.txt", 'a', encoding='utf-8-sig')
    f_a = open(base_dir + "infer/Online_A.txt", 'a', encoding='utf-8-sig')
    while True:
        seq = input("对Carol说些什么吧：")
        question_new = seq
        if seq == 'x':
            break
        seq = input_question(seq=seq, word_to_index=word_to_index, embed=embed)
        if type(seq) is str and seq.startswith("出现了Carol没法理解的词汇。。。："):
            continue
        with tf.device("/gpu:0"):
            answer = decode_greedy(
                seq=seq,
                question_model=question_model,
                answer_model=answer_model,
                word_to_index=word_to_index,
                index_to_word=index_to_word,
                embed=embed
            )
        #     answer=decode_beamsearch(seq, 3)
        print('ANSWER: ', answer)
        revision = input("是否修正？")
        if revision == 'y':
            answer_new = input("输入新回答")
            f_q.write(question_new + "\n")
            f_a.write(answer_new + "\n")
            f_q.flush()
            f_a.flush()
        while input("是否查找？") == 'y':
            if not use_keywords:
                must_include = input("必须包含：")
                exclude = input("不得包含：")
            else:
                must_include = ""
                exclude = ""
            for j in range(len(all_lines)):
                similar_answers_from_data = []
                for i in range(len(all_lines[j])):
                    line = all_lines[j][i]
                    line = line.replace(' ', '')
                    if "【禁用】" in lines[i]:
                        continue

                    # region use Similarity
                    if not use_keywords:
                        if len(exclude) >= 2 and exclude in line:
                            continue
                        if must_include in line:
                            scores = similarity_complex(line, answer)
                            scores, mean_score, max_score, std_score = scores
                            if max_score > 0.5:
                                similar_answers_from_data.append(i)
                                print(
                                    " 行号：", i + 1,
                                    " 内容：", line,
                                    " 最高分：", max_score
                                )
                    # endregion

                    # region Use Keywords
                    else:
                        i_o_u, matched = Keywords_IoU(answer, line)
                        if i_o_u >= 0.25 and matched >= 2:
                            similar_answers_from_data.append(i)
                            print(
                                " 行号：", i + 1,
                                " 内容：", line,
                                " IoU：", i_o_u,
                                " 相同：", matched
                            )
                    # endregion

                if j == 0:
                    if len(similar_answers_from_data) >= 1:
                        delete = input("是否禁用？")
                        if delete == 'y':
                            lines = mark_invalid(similar_answers_from_data, lines)
                            f_r.truncate(0)
                            f_r.seek(0)
                            f_r.writelines(lines)
                            f_r.flush()
                    else:
                        print("没有在查找到相似回答。")
    f_r.truncate(0)
    f_r.seek(0)
    f_r.writelines(lines)
    f_r.flush()
    f_r.close()
    f_q.close()
    f_a.close()


if __name__ == '__main__':
    GPU_list = tf.config.experimental.list_physical_devices('GPU')
    for gpu in GPU_list:
        tf.config.experimental.set_memory_growth(gpu, True)
    loop_talking()

import pickle
import tensorflow as tf
from tqdm import tqdm
from data.augmentation.similarity import similarity_complex, Keywords_IoU
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, dot, Activation, concatenate

from infer.utils import input_question, decode_greedy
from train.train_seq2seq import build_seq2seq
from train.utils import get_vocab_size, load_resource


def build_qa_model(wp=None):
    maxLen = 20
    iq, el, qh, qc, ld, iae, dd1, dd2, ia = build_seq2seq(
        vocab_size=get_vocab_size(),
        weight_path=wp
    )
    question_model = Model(iq, [el, qh, qc])
    question_model.summary()
    answer_h = Input(shape=(512,))
    answer_c = Input(shape=(512,))
    el = Input(shape=(maxLen, 512))
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


def loop_talking(UseKeywords=False):
    with open("../data/resource/raw/qingyun_withSyn.tsv", 'r+', encoding='utf-8-sig') as f_r:
        raw_lines = f_r.readlines()
    for i in tqdm(range(len(raw_lines))):
        raw_lines[i] = raw_lines[i].split('\t')[1].replace('\n', '').strip()
    question_model, answer_model = build_qa_model(wp="..\\train\\check_points\\W -109-0.0019-.h5")
    question, answer, answer_o, words, word_to_index, index_to_word = load_resource()
    f_q = open("Online_Q.txt", 'a', encoding='utf-8-sig')
    f_a = open("Online_A.txt", 'a', encoding='utf-8-sig')
    with open('../data/resource/composable.pkl', 'rb') as f:
        all_composable = pickle.load(f)
    while True:
        seq = input("对Carol说些什么吧：")
        question_new = seq
        if seq == 'x':
            break
        seq, sentence = input_question(seq=seq, word_to_index=word_to_index, all_composable=all_composable)
        print(sentence)
        if seq is None:
            continue
        with tf.device("/gpu:0"):
            answer = decode_greedy(
                seq=seq,
                sentence=sentence,
                question_model=question_model,
                answer_model=answer_model,
                word_to_index=word_to_index,
                index_to_word=index_to_word
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
            if not UseKeywords:
                must_include = input("必须包含：")
                exclude = input("不得包含：")
            else:
                must_include = ""
                exclude = ""
            similar_answers_from_data = []
            for i in range(len(raw_lines)):
                line = raw_lines[i]

                # region use Similarity
                if not UseKeywords:
                    if len(exclude) >= 2 and exclude in line:
                        continue
                    if must_include in line:
                        scores = similarity_complex(line, answer)
                        scores, mean_score, max_score, std_score = scores
                        if max_score > 0.5:
                            similar_answers_from_data.append(i)
                            print("行号：", i, " 内容：", line, " 最高分：", max_score)
                # endregion

                # region Use Keywords
                else:
                    i_o_u, matched = Keywords_IoU(answer, line)
                    if i_o_u >= 0.25 and matched >= 2:
                        similar_answers_from_data.append(i)
                        print()
                        print("行号：", i, " 内容：", line, " IoU：", i_o_u," 相同：", matched)
                # endregion
    f_q.close()
    f_a.close()


if __name__ == '__main__':
    loop_talking()

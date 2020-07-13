import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, dot, Activation, concatenate
from tqdm import tqdm

from data.augmentation.similarity import similarity_complex, Keywords_IoU
from infer.utils import input_question, decode_greedy
from obsolete.grammar4fluency import mark_invalid
from train.train_seq2seq import build_seq2seq
from train.utils import get_vocab_size, load_resource
from embed.w2v.w2v_emb_test import init_w2v
from embed.w2v.w2v_infer import input_question_w2v, decode_greedy_w2v


def build_qa_model(base_dir, wp=None, use_w2v=True):
    max_len = 20
    if use_w2v:
        w2v = init_w2v()
        iq, el, qh, qc, ld, iae, dd1, dd2, ia = build_seq2seq(
            base_dir=base_dir,
            vocab_size=len(w2v.index2word),
            weight_path=wp
        )
    else:
        iq, el, qh, qc, ld, iae, dd1, dd2, ia = build_seq2seq(
            base_dir=base_dir,
            vocab_size=get_vocab_size(base_dir=base_dir),
            weight_path=wp
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


def loop_talking(use_keywords=False, base_dir='../', use_w2v=True):
    f_r = open(base_dir + "data/resource/raw/all_corpus.tsv", 'r+', encoding='utf-8-sig')
    raw_lines = f_r.readlines()
    lines = raw_lines.copy()
    for i in tqdm(range(len(raw_lines))):
        raw_lines[i] = raw_lines[i].split('\t')[1].replace('\n', '').strip()
    all_lines = [raw_lines]
    question_model, answer_model = build_qa_model(
        base_dir=base_dir,
        wp=base_dir + "train/check_points/W - 85-0.0258-.h5",
        use_w2v=use_w2v
    )
    w2v = None
    if use_w2v:
        w2v = init_w2v()
    _, _, _, _, word_to_index, index_to_word = load_resource(base_dir=base_dir)
    f_q = open(base_dir + "infer/Online_Q.txt", 'a', encoding='utf-8-sig')
    f_a = open(base_dir + "infer/Online_A.txt", 'a', encoding='utf-8-sig')
    while True:
        seq = input("对Carol说些什么吧：")
        question_new = seq
        if seq == 'x':
            break
        if use_w2v:
            seq = input_question_w2v(seq=seq, w2v=w2v)
        else:
            seq = input_question(seq=seq, word_to_index=word_to_index)
        if type(seq) is str and seq.startswith("出现了Carol没法理解的词汇。。。："):
            continue
        with tf.device("/gpu:0"):
            if use_w2v:
                answer = decode_greedy_w2v(
                    seq=seq,
                    question_model=question_model,
                    answer_model=answer_model,
                    word2vec=w2v
                )
            else:
                answer = decode_greedy(
                    seq=seq,
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
    loop_talking()

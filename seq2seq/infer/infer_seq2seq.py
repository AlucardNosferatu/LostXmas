import tensorflow as tf
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


def loop_talking():
    question_model, answer_model = build_qa_model(wp="..\\train\\check_points\\W - 54-0.2819-.h5")
    question, answer, answer_o, words, word_to_index, index_to_word = load_resource()
    while True:
        seq = input()
        if seq == 'x':
            break
        seq, sentence = input_question(seq=seq, word_to_index=word_to_index)
        print(sentence)
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


if __name__ == '__main__':
    loop_talking()

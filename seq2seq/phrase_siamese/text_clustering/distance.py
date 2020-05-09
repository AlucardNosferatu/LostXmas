import sys
import os
import jieba
import tensorflow as tf
import numpy as np

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))))
from seq2seq.phrase.phrase_id_test import Phrase_Id_Map
from seq2seq.phrase.data_phrase import limit, EOS, PAD, pad_seq


def load_sentences(filename="seq2seq\\phrase_siamese\\text_clustering\\conv_zh.txt"):
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0])))
    os.chdir(root_path)
    idx_map = Phrase_Id_Map()
    f = open(filename, encoding='UTF-8-sig')
    sen_lines = f.readlines()
    f.close()
    return sen_lines, idx_map


def sen2vec(input_id_map, input_lines, count=None, pad=False):
    if count is None:
        count = len(input_lines)
    vec_temp = []
    for i in range(1, count, 2):
        line = input_lines[i].strip('\n')
        ask = input_lines[i - 1].strip('\n')
        line_list = jieba.lcut(line)
        ask_list = jieba.lcut(ask)
        if len(line_list) >= limit['maxa'] or len(ask_list) >= limit['maxq']:
            pass
        else:
            if pad:
                encode = pad_seq(line_list, input_id_map.w2idx, limit['maxa'], 2)
            else:
                encode = input_id_map.sentence2ids(line_list)
            vec_temp.append([line, encode])
    return vec_temp


def euc_distance(o1, o2, lookup, pad=True):
    l_o1 = o1.shape.as_list()[0]
    l_o2 = o2.shape.as_list()[0]
    o1 = tf.reshape(o1, (l_o1, 1))
    o2 = tf.reshape(o2, (l_o2, 1))

    if pad:
        length = limit['maxa'] - l_o2 - 1
        o2 = tf.pad(o2, [[0, 1], [0, 0]], "CONSTANT", constant_values=lookup[EOS])
        o2 = tf.pad(o2, [[0, length], [0, 0]], "CONSTANT", constant_values=lookup[PAD])
        length = limit['maxa'] - l_o1 - 1
        o1 = tf.pad(o1, [[0, 1], [0, 0]], "CONSTANT", constant_values=lookup[EOS])
        o1 = tf.pad(o1, [[0, length], [0, 0]], "CONSTANT", constant_values=lookup[PAD])

    o1 = tf.to_float(o1, name='ToFloat')
    o2 = tf.to_float(o2, name='ToFloat')

    eucd2 = tf.pow(tf.subtract(o1, o2), 2)
    eucd2 = tf.reduce_sum(eucd2, 0)
    eucd = tf.sqrt(eucd2, name="eucd")
    return eucd, eucd2


def vec_wrapper(input_vec):
    # vec is a list of vectorized sentence
    sen_array = np.array(input_vec)
    sen_tensor = tf.convert_to_tensor(sen_array)
    return sen_tensor


if __name__ == '__main__':
    lines, id_map = load_sentences()
    vec = sen2vec(input_id_map=id_map, input_lines=lines, count=10)
    tensor = vec_wrapper(vec[0][1])
    tensor2 = vec_wrapper(vec[1][1])
    sess = tf.Session()
    print(tensor.eval(session=sess))
    print(tensor2.eval(session=sess))
    d, d2 = euc_distance(tensor, tensor2, id_map.w2idx)
    print(d.eval(session=sess))
    print(d2.eval(session=sess))

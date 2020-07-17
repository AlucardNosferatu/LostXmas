import itertools

import numpy as np
import tensorflow as tf
from nltk.tokenize import sent_tokenize
from scipy import spatial
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing import sequence

from cfgs import epsilon_std


def split_into_sent(text):
    strg = ''
    for word in text:
        strg += word
        strg += ' '
    strg_cleaned = strg.lower()
    for x in ['\xd5d', '\n', '"', "!", '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>',
              '?', '@', '[', '^', ']', '_', '`', '{', '|', '}', '~', '\t']:
        strg_cleaned = strg_cleaned.replace(x, '')
    sentences = sent_tokenize(strg_cleaned)
    return sentences


def vectorize_sentences(w2v, sentences):
    vectorized = []
    for sentence in sentences:
        byword = sentence.split()
        concat_vector = []
        for word in byword:
            try:
                index = w2v.vocab[word].index
                concat_vector.append(index)
            except Exception as e:
                continue
                # print(repr(e))
                # print(word)
        vectorized.append(concat_vector)
    vectorized = sequence.pad_sequences(
        np.array(vectorized),
        maxlen=20,
        dtype='float32',
        padding='post',
        truncating='post',
        value=w2v.vocab['PAD'].index
    )
    return vectorized


def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(
        shape=(tf.shape(z_mean)[0], tf.shape(z_mean)[1]),
        mean=0.,
        stddev=epsilon_std
    )
    return z_mean + K.exp(z_log_var / 2) * epsilon


def zero_loss(y_true, y_pred):
    return K.zeros_like(y_pred)


def sent_parse(sentence, mat_shape, w2v):
    data_concat = []
    word_vecs = vectorize_sentences(w2v, sentence)
    for x in word_vecs:
        data_concat.append(list(itertools.chain.from_iterable(x)))
    zero_matr = np.zeros(mat_shape)
    zero_matr[0] = np.array(data_concat)
    return zero_matr


def print_sentence_with_w2v(sent_vect, w2v):
    sent_vect = np.squeeze(sent_vect)
    word_sent = ''
    for i in range(sent_vect.shape[0]):
        max_score = np.argmax(sent_vect[i])
        word_sent += w2v.index2word[max_score]
        word_sent += ' '
    # print(word_sent)
    return word_sent


def find_similar_encoding(sent_vect, sent_encoded):
    all_cosine = []
    for sent in sent_encoded:
        result = 1 - spatial.distance.cosine(sent_vect.reshape((-1)), sent.reshape((-1)))
        all_cosine.append(result)
    data_array = np.array(all_cosine)
    maximum = data_array.argsort()[-3:][::-1][1]
    new_vec = sent_encoded[maximum]
    return new_vec


def shortest_homology(point_one, point_two, num):
    dist_vec = point_two - point_one
    sample = np.linspace(0, 1, num, endpoint=True)
    hom_sample = []
    for s in sample:
        hom_sample.append(point_one + s * dist_vec)
    return hom_sample


def sent_2_sent(sent1, sent2, batch, dim, w2v, encoder, generator):
    a = sent_parse([sent1], (batch, dim), w2v)
    b = sent_parse([sent2], (batch, dim), w2v)
    encode_a = encoder.predict(a, batch_size=batch)
    encode_b = encoder.predict(b, batch_size=batch)
    test_hom = shortest_homology(encode_a[0], encode_b[0], 5)

    for point in test_hom:
        p = generator.predict(np.array([point]))[0]
        print_sentence_with_w2v(p, w2v)

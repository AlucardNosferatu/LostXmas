import itertools
import numpy as np
from scipy import spatial

from utils import vectorize_sentences


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
        sent_vect[i] = sent_vect[i] * 2 - 1
        word_sent += w2v.most_similar(positive=[sent_vect[i]], topn=1)[0][0]
        word_sent += ' '
    print(word_sent)


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

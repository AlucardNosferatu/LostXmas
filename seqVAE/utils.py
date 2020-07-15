import numpy as np
from nltk.tokenize import sent_tokenize
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import backend as K

from cfgs import batch_size, latent_dim, epsilon_std


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
                concat_vector.append(w2v[word])
            except Exception as e:
                print(repr(e))
                print(word)
        vectorized.append(concat_vector)
    vectorized = sequence.pad_sequences(
        np.array(vectorized),
        maxlen=20,
        dtype='float32',
        padding='post',
        truncating='post',
        value=w2v['PAD']
    )
    return vectorized


def sampling(args):
    z_mean, z_log_var = args
    epsilon = K.random_normal(
        shape=(batch_size, latent_dim),
        mean=0.,
        stddev=epsilon_std
    )
    return z_mean + K.exp(z_log_var / 2) * epsilon


def zero_loss(y_true, y_pred):
    return K.zeros_like(y_pred)
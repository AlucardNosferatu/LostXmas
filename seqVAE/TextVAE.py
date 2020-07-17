import os

import jieba
import numpy as np
import tensorflow as tf
from gensim.models import KeyedVectors
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from tqdm import tqdm

from cfgs import epochs, batch_size, seq_len, latent_dim
from model import build_vae, encoder_and_decoder
from utils import vectorize_sentences, shortest_homology, find_similar_encoding, print_sentence_with_w2v


def get_w2v():
    w2v = KeyedVectors.load_word2vec_format(
        'with_custom_corpus.vector',
        binary=False
    )
    w2v.init_sims(replace=True)
    return w2v


def get_data(w2v):
    text = []
    with open('Online_A.txt', mode='r', encoding='utf-8-sig') as f:
        text += f.readlines()
    with open('Online_Q.txt', mode='r', encoding='utf-8-sig') as f:
        text += f.readlines()
    with open('all_corpus.tsv', mode='r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            if not line.startswith('【禁用】'):
                text += line.split('\t')

    for i, line in enumerate(text):
        text[i] = ' '.join([item for item in jieba.lcut(line, cut_all=False) if item != '\n'])

    vect = vectorize_sentences(w2v, text)
    vect = vect.tolist()
    data = [x for x in vect if len(x) == seq_len]

    batch_length = int(len(data) / batch_size) * batch_size
    data_array = np.array(data)[:batch_length]
    np.random.shuffle(data_array)

    output_batch = data_array
    return output_batch


def train():
    w2v = get_w2v()
    train_batch = get_data(w2v)
    vae, x, z_mean, decoder_h, decoder_mean, _ = build_vae(
        len(w2v.index2word),
        w2v.get_keras_embedding()._initial_weights
    )
    if os.path.exists('weights.h5'):
        vae.load_weights(filepath='weights.h5')
    cp = [
        ModelCheckpoint(filepath="weights.h5", verbose=1, save_best_only=True, monitor='loss', save_weights_only=True),
        EarlyStopping(monitor='loss', patience=5, verbose=1),
        TensorBoard(log_dir='logs', histogram_freq=1, write_graph=True, write_images=True)
    ]
    with tf.device("/gpu:0"):
        vae.fit(
            train_batch,
            train_batch,
            shuffle=True,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=cp
        )


def gen():
    w2v = get_w2v()
    vae, x, z_mean, decoder_h, decoder_mean, repeated_context = build_vae(
        len(w2v.index2word),
        w2v.get_keras_embedding()._initial_weights
    )
    if os.path.exists('weights.h5'):
        vae.load_weights(filepath='weights.h5')
    encoder, generator = encoder_and_decoder(x, z_mean, decoder_h, decoder_mean, repeated_context)
    input_batch = get_data(w2v)
    # sent_encoded = encoder.predict(input_batch, batch_size=input_batch.shape[0])
    sent_encoded = encoder.predict(input_batch[:batch_size], batch_size=batch_size)
    sent_decoded = generator.predict(sent_encoded)
    for i in range(sent_decoded.shape[0]):
        print(i, ' ', print_sentence_with_w2v(sent_decoded[i], w2v))

    start_index = input("选定A语句编号")
    end_index = input("选定B语句编号")
    while not (start_index.isnumeric() and end_index.isnumeric() and 0 <= int(start_index) < batch_size and 0 <= int(
            end_index) < batch_size):
        start_index = input("选定A语句编号")
        end_index = input("选定B语句编号")
    start_index = int(start_index)
    end_index = int(end_index)
    print('################用隐变量合成语句################')
    test_hom = shortest_homology(sent_encoded[start_index], sent_encoded[end_index], 5)
    for point in test_hom:
        p = generator.predict(np.array([point]))[0]
        print(print_sentence_with_w2v(p, w2v))

    start_index = input("选定A语句编号")
    end_index = input("选定B语句编号")
    while not (start_index.isnumeric() and end_index.isnumeric() and 0 <= int(start_index) < batch_size and 0 <= int(
            end_index) < batch_size):
        start_index = input("选定A语句编号")
        end_index = input("选定B语句编号")
    start_index = int(start_index)
    end_index = int(end_index)
    print('################用隐变量合成语句################')
    test_hom = shortest_homology(sent_encoded[start_index], sent_encoded[end_index], 20)
    for point in test_hom:
        p = generator.predict(np.array([find_similar_encoding(point, sent_encoded)]))[0]
        print(print_sentence_with_w2v(p, w2v))


def from_random():
    w2v = get_w2v()
    vae, x, z_mean, decoder_h, decoder_mean, repeated_context = build_vae(
        len(w2v.index2word),
        w2v.get_keras_embedding()._initial_weights
    )
    if os.path.exists('weights.h5'):
        vae.load_weights(filepath='weights.h5')
    _, generator = encoder_and_decoder(x, z_mean, decoder_h, decoder_mean, repeated_context)
    while True:
        input_vec = np.random.rand(1, latent_dim)
        # print(input_vec)
        output_vec = generator.predict(input_vec, batch_size=1)
        print(print_sentence_with_w2v(output_vec, w2v))
        control = input("")
        if control == 'x':
            break


if __name__ == '__main__':
    # train()
    # gen()
    from_random()

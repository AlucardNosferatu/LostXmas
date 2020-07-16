import itertools

import jieba
import numpy as np
import tensorflow as tf
from gensim.models import KeyedVectors
from tensorflow.keras.callbacks import ModelCheckpoint

from cfgs import epochs, batch_size, seq_len
from gen import shortest_homology, find_similar_encoding, print_sentence_with_w2v
from model import build_vae, encoder_and_decoder
from utils import vectorize_sentences

w2v = KeyedVectors.load_word2vec_format(
    'with_custom_corpus.vector',
    binary=False
)

w2v.init_sims(replace=True)

data_concat = []
with open('Online_A.txt', mode='r', encoding='utf-8-sig') as f:
    text = f.readlines()

for i, line in enumerate(text):
    text[i] = ' '.join([item for item in jieba.lcut(line, cut_all=False) if item != '\n'])

vect = vectorize_sentences(w2v, text)
vect = vect.tolist()
data = [x for x in vect if len(x) == seq_len]
for x in data:
    data_concat.append(list(itertools.chain.from_iterable(x)))

data_array = np.array(data)
np.random.shuffle(data_array)

train = data_array
for i in range(train.shape[0]):
    print_sentence_with_w2v(train[i], w2v)
gpu_list = tf.config.experimental.list_physical_devices(device_type="GPU")
print(gpu_list)
for gpu in gpu_list:
    tf.config.experimental.set_memory_growth(gpu, True)
cp = [ModelCheckpoint(filepath="model.h5", verbose=1, save_best_only=True, monitor='loss')]
vae, x, z_mean, decoder_h, decoder_mean = build_vae()
with tf.device("/gpu:0"):
    vae.fit(
        train,
        train,
        shuffle=True,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=cp
    )
encoder, generator = encoder_and_decoder(x, z_mean, decoder_h, decoder_mean)
sent_encoded = encoder.predict(np.array(train), batch_size=50)
sent_decoded = generator.predict(sent_encoded)
for i in range(sent_decoded.shape[0]):
    print_sentence_with_w2v(sent_decoded[i], w2v)


test_hom = shortest_homology(sent_encoded[3], sent_encoded[10], 5)
for point in test_hom:
    p = generator.predict(np.array([point]))[0]
    print_sentence_with_w2v(p, w2v)

test_hom = shortest_homology(sent_encoded[2], sent_encoded[40], 20)
for point in test_hom:
    p = generator.predict(np.array([find_similar_encoding(point, sent_encoded)]))[0]
    print_sentence_with_w2v(p, w2v)

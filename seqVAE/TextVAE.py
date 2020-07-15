import itertools

import jieba
import numpy as np
from gensim.models import KeyedVectors

from cfgs import epochs, batch_size
from model import build_vae
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
data = [x for x in vect if len(x) == 20]
for x in data:
    data_concat.append(list(itertools.chain.from_iterable(x)))

data_array = np.array(data_concat)
np.random.shuffle(data_array)

train = data_array

vae = build_vae()
vae.fit(
    train,
    train,
    shuffle=True,
    epochs=epochs,
    batch_size=batch_size,
)

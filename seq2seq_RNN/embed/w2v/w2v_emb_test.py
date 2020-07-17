import random

import gensim
import numpy as np


def process_corpus():
    name_list = ['刘真']
    with open('news_sohusite_xml.dat', mode='r', encoding='gb18030') as f:
        sentence = f.readline()
        with open('corpus_1.txt', mode='r+', encoding='utf-8-sig') as f2:
            lines = f2.readlines()
            already = len(lines)
            while sentence:
                if sentence.startswith('<content>'):
                    sentence = sentence.replace('<content>', '').replace('</content>', '').replace("", "")
                    if sentence != '\n':
                        if already != 0:
                            already -= 1
                            continue
                        else:
                            for name in name_list:
                                if len(name) > 1:
                                    sentence = sentence.replace(name, random.choice(['Scrooge', 'Carol']))
                            # lines.append(sentence)
                        if len(lines) % 100 == 0 or True:
                            # print(len(lines))
                            # f2.truncate(0)
                            # f2.seek(0)
                            f2.writelines([sentence])
                            f2.flush()
                sentence = f.readline()
            print("Done")


def init_w2v(base_dir="../"):
    try:
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(
            base_dir + 'w2v/with_custom_corpus.vector',
            binary=False
        )
    except OSError:
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(
            base_dir + 'w2v/corpusSegDone_1.vector',
            binary=False
        )
    # word2vec.init_sims(replace=True)
    return word2vec


def word2vector(word, word2vec):
    dims = word2vec.vector_size
    if word in word2vec.vocab:
        vector = word2vec.wv.word_vec(word, use_norm=True)
    else:
        vector = np.zeros(shape=(dims,))
    return vector


def word2index(word, word2vec):
    if word in word2vec.wv.vocab:
        index = word2vec.wv.vocab[word].index
    else:
        index = word2vec.wv.vocab['UNK'].index
    return index


def get_embedding(w2v=None):
    if w2v is None:
        w2v = init_w2v()
    ke = w2v.wv.get_keras_embedding(train_embeddings=False)
    weights = ke._initial_weights
    return weights


if __name__ == '__main__':
    print("Done")

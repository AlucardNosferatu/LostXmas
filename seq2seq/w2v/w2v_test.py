import random

import gensim
import numpy as np
import Neu
from snownlp import SnowNLP


def process_corpus():
    lines = []
    with open('news_sohusite_xml.dat', mode='r', encoding='gb18030') as f:
        sentence = f.readline()
        with open('corpus_1.txt', mode='w', encoding='utf-8-sig') as f2:
            while sentence:
                if sentence.startswith('<content>'):
                    sentence = sentence.replace('<content>', '').replace('</content>', '').replace("", "")
                    name_list = ['刘真']
                    for name in name_list:
                        if len(name) > 1:
                            sentence = sentence.replace(name, random.choice(['Scrooge', 'Carol']))
                    if sentence != '\n':
                        lines.append(sentence)
                        f2.truncate(0)
                        f2.seek(0)
                        f2.writelines(lines)
                        f2.flush()
                        print(len(lines))
                sentence = f.readline()
            f2.truncate(0)
            f2.seek(0)
            f2.writelines(lines)
            f2.flush()
            print("Done")


def init_w2v(base_dir="../"):
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(
        base_dir + 'w2v/corpusSegDone_1.vector',
        binary=False
    )
    word2vec.init_sims(replace=True)
    return word2vec


def word2vector(word, word2vec):
    dims = word2vec.vector_size
    if word in word2vec.vocab:
        vector = word2vec.wv.word_vec(word, use_norm=True)
    else:
        vector = np.zeros(shape=(dims,))
    return vector


if __name__ == '__main__':
    process_corpus()
    print("Done")

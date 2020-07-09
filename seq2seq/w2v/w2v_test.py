import gensim
import numpy as np

def process_corpus():
    lines = []
    with open('news_sohusite_xml.dat', mode='r', encoding='gb18030') as f:
        line = f.readline()
        while line:
            if line.startswith('<content>'):
                line = line.replace('<content>', '').replace('</content>', '')
                if line != '\n':
                    lines.append(line)
            line = f.readline()
        with open('corpus_1.txt', mode='w', encoding='utf-8-sig') as f2:
            f2.writelines(lines)
        print("Done")


def init_w2v(base_dir="../"):
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(
        base_dir + 'w2v/corpusSegDone_1.vector',
        binary=False
    )
    return word2vec


def word2vector(word, word2vec):
    dims = word2vec.vector_size
    if word in word2vec.vocab:
        vector = word2vec.get_vector(word)
    else:
        vector = np.zeros(shape=(dims,))
    return vector


if __name__ == '__main__':
    w2v = gensim.models.KeyedVectors.load_word2vec_format('corpusSegDone_1.vector', binary=False)
    vec = w2v.get_vector('的')
    print("Done")

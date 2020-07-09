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


if __name__ == '__main__':
    word2vec = gensim.models.KeyedVectors.load_word2vec_format('corpusSegDone_1.vector', binary=False)
    vector = word2vec.get_vector('的')
    print("Done")

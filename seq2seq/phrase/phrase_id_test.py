import numpy as np
import pickle


class Phrase_Id_Map(object):
    idx2w = None
    w2idx = None

    def __init__(self):
        with open('seq2seq\\phrase\\idx2p.pkl', 'rb') as f:
            self.idx2w = pickle.load(f)

        with open('seq2seq\\phrase\\p2idx.pkl', 'rb') as f:
            self.w2idx = pickle.load(f)

    def sentence2ids(self, sentence):
        ids = []
        for word in sentence:
            ids.append(self.w2idx[word])
        return ids

    def ids2sentence(self, ids):
        sentence = []
        for id in ids:
            sentence.append(self.idx2w[id])
        return sentence


def main():
    map = Phrase_Id_Map()
    ids = map.sentence2ids(['hello', 'world', "are", "you", "ok", 'i', 'am', 'ok'])
    print(ids)
    sentence = map.ids2sentence(ids)
    print(sentence)
    print(map.idx2w[0])
    train_x = np.load('./idx_q_phrase.npy', mmap_mode='r')
    print(train_x)
    print(map.ids2sentence(train_x[5]))
    train_y = np.load('./idx_a_phrase.npy', mmap_mode='r')
    print(train_y)
    print(map.ids2sentence(train_y[5]))


if __name__ == "__main__":
    main()

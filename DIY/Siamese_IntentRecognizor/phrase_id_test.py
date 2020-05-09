import numpy as np
import pickle


class PhraseIdMap(object):
    idx2w = None
    w2idx = None

    def __init__(self):
        with open('RASA_data\\idx2p.pkl', 'rb') as f:
            self.idx2w = pickle.load(f)

        with open('RASA_data\\p2idx.pkl', 'rb') as f:
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
    map_instance = PhraseIdMap()
    ids = map_instance.sentence2ids(['hello', 'world', "are", "you", "ok", 'i', 'am', 'ok'])
    print(ids)
    sentence = map_instance.ids2sentence(ids)
    print(sentence)
    print(map_instance.idx2w[0])


if __name__ == "__main__":
    main()

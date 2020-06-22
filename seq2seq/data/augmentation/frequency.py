import jieba
from nltk.probability import FreqDist
from tqdm import tqdm

from data.data_tool import Traditional2Simplified


def getFreqDist(words_with_dup):
    fdist = FreqDist(words_with_dup)
    fdist = sorted(fdist.items(), key=lambda item: item[1], reverse=True)
    fdist = [item[0] for item in fdist]
    return fdist


def getWords():
    a = open('../resource/raw/legacy/answer.txt', 'r', encoding='utf-8-sig')
    a_out = open('../resource/raw/legacy/a_compact_vocab.txt', 'r', encoding='utf-8-sig')
    q = open('../resource/raw/legacy/question.txt', 'r', encoding='utf-8-sig')
    q_out = open('../resource/raw/legacy/q_compact_vocab.txt', 'r', encoding='utf-8-sig')
    a_sentences = a.readlines()
    a_out_sentences = a_out.readlines()
    q_sentences = q.readlines()
    q_out_sentences = q_out.readlines()
    a.close()
    a_out.close()
    q.close()
    q_out.close()
    for sentences in [a_sentences + q_sentences, a_out_sentences + q_out_sentences]:
        words_with_dup = []
        for i in tqdm(range(len(sentences))):
            words = jieba.lcut(Traditional2Simplified(sentences[i]).strip(), cut_all=False)
            words_with_dup += words
        fdist = getFreqDist(words_with_dup)
        print()
        print(len(fdist))


if __name__ == "__main__":
    getWords()

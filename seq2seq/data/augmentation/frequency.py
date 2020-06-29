import jieba
from nltk.probability import FreqDist
from tqdm import tqdm

from data.data_tool import Traditional2Simplified


def getFreqDist(words_with_dup):
    fdist = FreqDist(words_with_dup)
    fdist = sorted(fdist.items(), key=lambda item: item[1], reverse=True)
    fdist = [item[0] for item in fdist]
    return fdist


def getWordsFromFiles():
    a = open('../resource/raw/legacy/Soliq_A.txt', 'r', encoding='utf-8-sig')
    a_out = open('../resource/raw/legacy/compact_vocab_A.txt', 'r', encoding='utf-8-sig')
    q = open('../resource/raw/legacy/Soliq_Q.txt', 'r', encoding='utf-8-sig')
    q_out = open('../resource/raw/legacy/compact_vocab_Q.txt', 'r', encoding='utf-8-sig')
    a_sentences = a.readlines()
    a_out_sentences = a_out.readlines()
    q_sentences = q.readlines()
    q_out_sentences = q_out.readlines()
    a.close()
    a_out.close()
    q.close()
    q_out.close()
    fdist_list = []
    wwd = []
    for sentences in [a_sentences + q_sentences, a_out_sentences + q_out_sentences]:
        words_with_dup = []
        for i in tqdm(range(len(sentences))):
            words = jieba.lcut(Traditional2Simplified(sentences[i]).strip(), cut_all=False)
            words_with_dup += words
        wwd.append(words_with_dup)
        fdist = getFreqDist(words_with_dup)
        fdist_list.append(fdist)
    return wwd, fdist_list


def getWords(lines):
    words_with_dup = []
    for line in lines:
        words = line.split(' ')
        words_with_dup += words
    freq_dist = getFreqDist(words_with_dup)
    return words_with_dup, freq_dist


if __name__ == "__main__":
    getWordsFromFiles()

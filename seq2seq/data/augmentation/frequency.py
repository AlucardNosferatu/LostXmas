from nltk.probability import FreqDist


def getFreqDist(words_with_dup):
    fdist = FreqDist(words_with_dup)
    fdist = sorted(fdist.items(), key=lambda item: item[1], reverse=True)
    fdist = [item[0] for item in fdist]
    return fdist

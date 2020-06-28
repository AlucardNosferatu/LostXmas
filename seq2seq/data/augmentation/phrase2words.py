from data.augmentation.frequency import getWordsFromFiles
from data.data_tool import is_all_chinese


def getBaseWord(freq_dist):
    base_words = []
    for word in freq_dist[:int(0.2 * len(freq_dist))]:
        if is_all_chinese(word) and len(word) == 1:
            base_words.append(word)
    return base_words


def getComposed(base_word, freq_dist):
    all_composed = []
    for phrase in freq_dist[int(0.2 * len(freq_dist)):]:
        be_composed = True
        if is_all_chinese(phrase) and len(phrase) > 1:
            for word in phrase:
                if word in base_word:
                    continue
                else:
                    be_composed = False
                    break
            if be_composed:
                all_composed.append(phrase)
    return all_composed


if __name__ == "__main__":
    _, freq_dists = getWordsFromFiles()
    FD = freq_dists[0]
    baseWord = getBaseWord(FD)
    AllComposed = getComposed(baseWord, FD)
    print("Done")

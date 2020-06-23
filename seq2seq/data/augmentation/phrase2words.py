from data.augmentation.frequency import getWordsFromFiles
from data.data_tool import is_all_chinese


def getBaseWord(fdist):
    baseWords = []
    for word in fdist[:100]:
        if is_all_chinese(word) and len(word) == 1:
            baseWords.append(word)
    return baseWords


def getComposable(baseWord, fdist):
    AllComposable = []
    for phrase in fdist[50:]:
        composable = True
        if is_all_chinese(phrase) and len(phrase) > 1:
            for word in phrase:
                if word in baseWord:
                    continue
                else:
                    composable = False
                    break
            if composable:
                AllComposable.append(phrase)
    return AllComposable


if __name__ == "__main__":
    _, fdist_list = getWordsFromFiles()
    fdist = fdist_list[0]
    baseWord = getBaseWord(fdist)
    AllComposable = getComposable(baseWord, fdist)
    print("Done")

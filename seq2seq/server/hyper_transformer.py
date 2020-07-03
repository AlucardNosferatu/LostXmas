import copy
import jieba
import synonyms

from train.utils import load_resource


def input_question(seq="还须努力", BaseDir='../'):
    _, _, _, _, word_to_index, _ = load_resource(BaseDir=BaseDir)
    seq = seq.replace('，', ',').replace('。', '.')
    seq = jieba.lcut(seq.strip(), cut_all=False)
    for k in range(len(seq)):
        if not seq[k] in word_to_index:
            seq[k] = translate(word_to_index, seq[k])
    return seq


def translate(word_to_index, word, blacklist=[]):
    assert type(word) is str
    word = list(word)
    for i in range(len(word)):
        each = word[i]
        assert len(each) == 1
        if each in word_to_index:
            continue
        else:
            syn = copy.deepcopy(list(synonyms.nearby(each)))
            if len(syn[0]) == 0:
                continue
            del syn[0][0]
            del syn[1][0]
            for used in blacklist:
                if used in syn[0]:
                    index = syn[0].index(used)
                    del syn[0][index]
                    del syn[1][index]
            each = syn[0][syn[1].index(max(syn[1]))]
            if each in word_to_index:
                return each
            else:
                blacklist.append(each)
                each = translate(word_to_index, each, blacklist)
            return each
    return ''.join(word)


if __name__ == '__main__':
    seq = input_question()
    print(seq)

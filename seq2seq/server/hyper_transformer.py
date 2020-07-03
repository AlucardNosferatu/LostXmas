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
    blacklist = list(set(blacklist))
    assert type(word) is str
    syn_list = copy.deepcopy(list(synonyms.nearby(word)))
    if len(syn_list[0]) == 0 or len(blacklist) >= 5:
        word = ""
    else:
        del syn_list[0][0]
        del syn_list[1][0]
        for used in blacklist:
            i = 0
            while i < len(syn_list[0]):
                if used in syn_list[0][i]:
                    del syn_list[0][i]
                    del syn_list[1][i]
                else:
                    i += 1
        word = syn_list[0][syn_list[1].index(max(syn_list[1]))]
    if word in word_to_index:
        return word
    blacklist.append(word)
    word = list(word)
    temp = []
    exceed_size_limit = False
    for i in range(len(word)):
        each = word[i]
        assert len(each) == 1
        if each in word_to_index:
            continue
        else:
            blacklist.append(each)
            each = translate(word_to_index, each, blacklist)
            if len(each.replace(' ', '')) > 3:
                exceed_size_limit = True
                temp = each.split(' ')
                break
        word[i] = each
    if exceed_size_limit:
        word = temp
    return ' '.join(word)


if __name__ == '__main__':
    seq = input_question()
    print(seq)

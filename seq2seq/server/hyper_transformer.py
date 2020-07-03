import copy
import jieba
import synonyms

from train.utils import load_resource


def input_question(seq="下馆子", base_dir='../'):
    _, _, _, _, word_to_index, _ = load_resource(BaseDir=base_dir)
    seq = seq.replace('，', ',').replace('。', '.')
    seq = jieba.lcut(seq.strip(), cut_all=False)
    for k in range(len(seq)):
        if not seq[k] in word_to_index:
            seq[k] = recursive_translator(word_to_index, seq[k], 0)
    seq = ' '.join(seq)
    return seq


def syn_replacer(word_to_index, word, most_similar=False):
    if word in word_to_index:
        return word
    syn_list = copy.deepcopy(synonyms.nearby(word))
    if len(syn_list[0]) == 0:
        return word
    del syn_list[0][0]
    del syn_list[1][0]
    i = 0
    for syn in syn_list[0]:
        if syn in word_to_index:
            return syn
    if most_similar:
        while i < len(syn_list[0]):
            if word in syn_list[0][i]:
                del syn_list[0][i]
                del syn_list[1][i]
            else:
                i += 1
        word = syn_list[0][syn_list[1].index(max(syn_list[1]))]
    return word


def decompose(word_to_index, word):
    word = list(word)
    i = 0
    while i < len(word):
        if word[i] in word_to_index:
            i += 1
        else:
            syn = syn_replacer(word_to_index, word[i])
            if syn == word[i]:
                del word[i]
            else:
                word[i] = syn
    word = ' '.join(word)
    return word


def translator(word_to_index, word):
    syn = syn_replacer(word_to_index, word)
    if syn == word:
        word = decompose(word_to_index, word)
    else:
        word = syn
    return word


def recursive_translator(word_to_index, word, count=0):
    word = syn_replacer(word_to_index, word, True)
    if count > 3 or word in word_to_index:
        return word
    else:
        word = list(word)
        count += len(word)
        for i in range(len(word)):
            word[i] = recursive_translator(word_to_index, word[i], count)
        word = ' '.join(word)
    return word


if __name__ == '__main__':
    seq = input_question()
    print(seq)

import jieba
from chinese_synonym_word.chinese_synonym_word import chinese_synonym_word
from tqdm import tqdm

from data.augmentation.frequency import getFreqDist
from data.data_tool import Traditional2Simplified


def sym_of_word(word):
    syms = chinese_synonym_word.get_synonym_word_cl(word, is_strict=True)
    if syms and len(syms) > 1:
        syms = syms[:max(min(int(len(syms) / 4), 3), 1)]
        if word in syms:
            del syms[syms.index(word)]
    else:
        syms = []
    return syms


def compress_vocab(vocab, freq_dist):
    print("压缩前：", len(vocab))
    kill_list = []
    white_list = []
    for key in freq_dist:
        if freq_dist.index(key) < 0.25 * len(freq_dist):
            white_list.append(key)
        if key in kill_list:
            pass
        else:
            syms = vocab[key]
            for sym in syms:
                if sym in vocab:
                    kill_list.append(sym)
                    white_list.append(key)
    for dead in kill_list:
        if (dead in vocab) and not (dead in white_list):
            del vocab[dead]
    print("压缩后：", len(vocab))
    return vocab


def simplify_sentence(sentence, vocab):
    words = jieba.lcut(Traditional2Simplified(sentence).strip(), cut_all=False)
    for j in range(len(words)):
        if words[j] in vocab:
            pass
        else:
            k = 0
            while k < len(list(vocab.keys())):
                key = list(vocab.keys())[k]
                if words[j] in vocab[key]:
                    temp_words = words.copy()
                    temp_words[j] = key
                    temp = "".join(temp_words)
                    print("替换前：", "".join(words))
                    print("替换后：", temp)
                    choice = input("?")
                    if choice == 'y':
                        words = temp_words
                        k += 1
                    elif choice == 'n':
                        k += 1
                    else:
                        pass
                else:
                    k += 1
    temp = "".join(words)
    sentence = temp + "\n"
    return sentence


def simplify():
    # f = open('../resource/raw/legacy/Soliq_Q.txt', 'r', encoding='utf-8-sig')
    # f_out = open('../resource/raw/legacy/compact_vocab_Q.txt', 'a', encoding='utf-8-sig')
    f = open('legacy/Soliq_A.txt', 'r', encoding='utf-8-sig')
    f_out = open('legacy/compact_vocab_A.txt', 'a', encoding='utf-8-sig')
    sentences = f.readlines()
    f.close()
    vocab = {}
    words_with_dup = []
    for i in tqdm(range(len(sentences))):
        words = jieba.lcut(Traditional2Simplified(sentences[i]).strip(), cut_all=False)
        words_with_dup += words
        for word in words:
            vocab[word] = sym_of_word(word)
    fdist = getFreqDist(words_with_dup)
    vocab = compress_vocab(vocab, fdist)

    for i in range(len(sentences)):
        words = jieba.lcut(Traditional2Simplified(sentences[i]).strip(), cut_all=False)
        for j in range(len(words)):
            if words[j] in vocab:
                pass
            else:
                k = 0
                while k < len(list(vocab.keys())):
                    key = list(vocab.keys())[k]
                    if words[j] in vocab[key]:
                        temp_words = words.copy()
                        temp_words[j] = key
                        temp = "".join(temp_words)
                        print("替换前：", "".join(words))
                        print("替换后：", temp)
                        choice = input("?")
                        if choice == 'y':
                            words = temp_words
                            k += 1
                        elif choice == 'n':
                            k += 1
                        else:
                            pass
                    else:
                        k += 1
        temp = "".join(words)
        sentences[i] = temp + "\n"
        f_out.write(sentences[i])
        f_out.flush()
    f_out.close()

    return sentences


if __name__ == "__main__":
    simplify()

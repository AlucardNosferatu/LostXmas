import jieba
from tqdm import tqdm
import numpy as np
from data.augmentation.blacklist import DFAFilter
from data.data_tool import append_extra_data, is_all_chinese, is_pure_english, remove_brackets, remove_banned, \
    Traditional2Simplified
from embed.w2v.w2v_emb_test import init_w2v, word2index
from embed.w2v.w2v_emb_train import incremental_train


def w2v_packer(base_dir="../", inc_train=False):
    gfw = DFAFilter()
    gfw.parse(base_dir + 'data/augmentation/blacklist')

    # region Append test log
    q_path = base_dir + 'infer/Online_Q_SIAW.txt'
    a_path = base_dir + 'infer/Online_A_SIAW.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, [], [])
    # endregion

    # region get Q&A
    with open(base_dir + 'data/resource/raw/all_corpus.tsv', 'r', encoding='utf-8-sig') as f:
        lines = f.read().split('\n')
        lines = lines[:-2]
        lines = remove_brackets(lines)
        lines = remove_banned(lines)

    for i in tqdm(range(len(lines))):
        line = lines[i]
        if '\t' not in line:
            continue
        line = line.split('\t')
        q = line[0].strip()
        a = line[1].strip()
        if 'Carol' in q + a or '守财奴' in q + a:
            pass
        else:
            q_filter = gfw.filter(q, '*')
            a_filter = gfw.filter(a, '*')
            if q_filter[1] or a_filter[1]:
                continue
        question.append(' '.join(jieba.lcut(Traditional2Simplified(q).strip(), cut_all=False)))
        answer.append(' '.join(jieba.lcut(Traditional2Simplified(a).strip(), cut_all=False)))
    # endregion

    # region Process special chars
    character = set()
    for seq in tqdm(question + answer):
        word_list = seq.split(' ')
        for word in word_list:
            if not is_all_chinese(word):
                character.add(word)
    character = list(character)
    stop_words = set()
    for pos, word in enumerate(tqdm(character)):
        if not is_pure_english(word):
            stop_words.add(word)
    max_len = 18
    # endregion

    stop_words = set()

    # region Process questions
    for pos, seq in enumerate(tqdm(question)):
        seq = seq.replace('  ', ' , ')
        seq_list = seq.split(' ')
        while '' in seq_list:
            del seq_list[seq_list.index('')]
        while '\ufeff' in seq_list:
            del seq_list[seq_list.index('\ufeff')]
        for pos_, word in enumerate(seq_list):
            if len(word) > 1 and word.isnumeric():
                seq_list[pos_] = ' '.join(list(word))
            if word in stop_words:
                seq_list.pop(pos_)
        seq_list = ' '.join(seq_list)
        seq_list = seq_list.split(' ')
        if len(seq_list) > max_len:
            seq_list = seq_list[:max_len]
        question[pos] = ' '.join(seq_list)
    # endregion

    # region Process answers
    for pos, seq in enumerate(tqdm(answer)):
        seq = seq.replace('  ', ' , ')
        seq_list = seq.split(' ')
        while '' in seq_list:
            del seq_list[seq_list.index('')]
        while '\ufeff' in seq_list:
            del seq_list[seq_list.index('\ufeff')]
        for pos_, word in enumerate(seq_list):
            if len(word) > 1 and word.isnumeric():
                seq_list[pos_] = ' '.join(list(word))
            if word in stop_words:
                seq_list.pop(pos_)
        seq_list = ' '.join(seq_list)
        seq_list = seq_list.split(' ')
        if len(seq_list) > max_len:
            seq_list = seq_list[:max_len]
        answer[pos] = ' '.join(seq_list)
    # endregion

    answer_a = ['BOS ' + i + ' EOS' for i in answer]
    answer_b = [i + ' EOS' for i in answer]

    for i in range(len(answer_a)):
        temp = answer_a[i].split(' ')
        while len(temp) < 20:
            temp.append('PAD')
        answer_a[i] = ' '.join(temp)

    for i in range(len(question)):
        temp = question[i].split(' ')
        while len(temp) < 20:
            temp.append('PAD')
        question[i] = ' '.join(temp)

    if inc_train:
        incremental_train(
            more_sentences=question + answer_a,
            base_dir="../../"
        )
    w2v = init_w2v()

    for i in range(len(answer_a)):
        words = answer_a[i].split(' ')
        for j in range(len(words)):
            if words[j] not in w2v.vocab:
                words[j] = 'UNK'
        answer_a[i] = ' '.join(words)

    for i in range(len(question)):
        words = question[i].split(' ')
        for j in range(len(words)):
            if words[j] not in w2v.vocab:
                words[j] = 'UNK'
        question[i] = ' '.join(words)

    if inc_train:
        incremental_train(
            more_sentences=question + answer_a,
            base_dir="../../"
        )
        w2v = init_w2v()
    assert 'UNK' in w2v.vocab
    question = np.array([[word2index(w, w2v) for w in i.split(' ')] for i in question])
    answer_a = np.array([[word2index(w, w2v) for w in i.split(' ')] for i in answer_a])
    answer_b = np.array([[word2index(w, w2v) for w in i.split(' ')] for i in answer_b])

    size = int(len(question) / 100) * 100
    question = question[:size]
    answer_a = answer_a[:size]
    answer_b = answer_b[:size]
    np.save(base_dir + 'data/resource/answer_o.npy', answer_b)
    np.save(base_dir + 'data/resource/pad_question.npy', question)
    np.save(base_dir + 'data/resource/pad_answer.npy', answer_a)


if __name__ == '__main__':
    w2v_packer()

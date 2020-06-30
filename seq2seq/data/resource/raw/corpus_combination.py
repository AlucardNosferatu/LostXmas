from tqdm import tqdm

from data.augmentation.blacklist import DFAFilter
from data.data_tool import append_extra_data


def getExtra():
    gfw = DFAFilter()
    gfw.parse('../../augmentation/blacklist')
    q_path = 'legacy/compact_vocab_Q.txt'
    a_path = 'legacy/compact_vocab_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, [], [])
    q_path = 'legacy/CPoL4OC_Q.txt'
    a_path = 'legacy/CPoL4OC_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'legacy/Lovers_Q.txt'
    a_path = 'legacy/Lovers_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'legacy/MyTulpa_Q.txt'
    a_path = 'legacy/MyTulpa_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'legacy/XiaoIce_Q.txt'
    a_path = 'legacy/XiaoIce_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'legacy/YellowChick_Q.txt'
    a_path = 'legacy/YellowChick_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = 'legacy/ChatterBot_Q.txt'
    a_path = 'legacy/ChatterBot_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)
    q_path = '../../../infer/Online_Q.txt'
    a_path = '../../../infer/Online_A.txt'
    question, answer = append_extra_data(gfw, q_path, a_path, question, answer)

    f = open('all_corpus.tsv', 'w', encoding='utf-8-sig')
    lines = []
    for i in tqdm(range(len(question))):
        line = question[i].replace(' ', '') + " \t " + answer[i].replace(' ', '') + '\n'
        f.write(line)
        f.flush()
    f.close()


def getQingYun():
    f_q = open('../../obsolete/qingyun_withSyn.tsv', 'r', encoding='utf-8-sig')
    lines = f_q.readlines()
    f_q.close()
    f_a = open('all_corpus.tsv', 'a', encoding='utf-8-sig')
    for line in tqdm(lines):
        if line.startswith('【禁用】'):
            continue
        f_a.write(line)
        f_a.flush()
    f_a.close()


if __name__ == '__main__':
    getQingYun()

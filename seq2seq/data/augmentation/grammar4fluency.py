import pycorrector
from ltp import LTP
from tqdm import tqdm

from data.data_tool import is_all_chinese


def batch_mark(QingYun=False):
    nlp = LTP()
    # pycorrector.enable_char_error(enable=False)
    if QingYun:
        text_path = "../resource/raw/qingyun_withSyn.tsv"
    else:
        text_path = "../resource/raw/legacy/YellowChick_Q.txt"
        # text_path = "../../infer/Online_Q.txt"
    with open(text_path, 'r+', encoding='utf-8-sig') as f_q:
        with open("../resource/raw/legacy/YellowChick_A.txt", 'r+', encoding='utf-8-sig') as f_a:
            # with open("../../infer/Online_A.txt", 'r+', encoding='utf-8-sig') as f_a:
            q_lines = f_q.readlines()
            a_lines = f_a.readlines()
            for i in tqdm(range(len(q_lines))):
                if q_lines[i].startswith('【禁用】'):
                    continue
                if QingYun:
                    q = q_lines[i].split('\t')[0].strip()
                    a = q_lines[i].split('\t')[1].replace('\n', '').strip()
                else:
                    q = q_lines[i].replace('\n', '')
                    a = a_lines[i].replace('\n', '')
                perplexity, corrected_sent = perplexity_detection(a)
                has_error = grammar_analysis(a, nlp)
                if perplexity or has_error:
                    # print(i, q, a, '\n')
                    # choice = input('是否删去？')
                    choice = 'y'
                    if choice == 'c':
                        if QingYun:
                            q_lines[i] = q_lines[i].replace(a, corrected_sent)
                        else:
                            a_lines[i] = a_lines[i].replace(a, corrected_sent)
                    elif choice == 'y':
                        if QingYun:
                            pass
                        else:
                            a_lines[i] = '【禁用】' + a_lines[i]
                        q_lines[i] = '【禁用】' + q_lines[i]
                    elif choice == 'q':
                        break
                else:
                    pass
            f_q.truncate(0)
            f_q.seek(0)
            f_q.writelines(q_lines)
            if QingYun:
                pass
            else:
                f_a.truncate(0)
                f_a.seek(0)
                f_a.writelines(a_lines)


def grammar_analysis(sentence, parser):
    try:
        segment, hidden = parser.seg([sentence])
    except Exception as e:
        print(repr(e))
        return True
    ner = parser.ner(hidden)
    # pos = parser.pos(hidden)
    # srl = parser.srl(hidden)
    # dep = parser.dep(hidden)
    # sdp = parser.sdp(hidden)
    # suspicion = srl[0].count([]) == len(segment[0])
    # suspicion = len(ner[0]) != 0 or suspicion
    suspicion = len(ner[0]) != 0
    if suspicion:
        pass
        # print(segment)
        # print("NER: ", ner)
        # print("POS: ", pos)
        # print("SRL: ", srl)
        # print("DEP: ", dep)
        # print("SDP: ", sdp)
    return suspicion


def perplexity_detection(src):
    corrected_sent = src
    # print(src)
    # corrected_sent, detail = pycorrector.correct(src)
    # idx_errors = pycorrector.detect(src)
    # detected = (len(idx_errors) != 0)
    detected = False
    if detected:
        pass
        # print(idx_errors)
        # print(corrected_sent, detail)
    return detected, corrected_sent


def mark_invalid(invalid_indices, lines):
    for i in invalid_indices:
        lines[i] = "【禁用】" + lines[i]
    return lines


if __name__ == '__main__':
    batch_mark()

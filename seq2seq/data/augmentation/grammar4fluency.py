import pycorrector
from ltp import LTP
from tqdm import tqdm


def batch_mark():
    nlp = LTP()
    text_path = "../resource/raw/all_in_one.tsv"
    with open(text_path, 'r+', encoding='utf-8-sig') as f_q:
        q_lines = f_q.readlines()
        # for i in tqdm(range(453000, len(q_lines))):
        for i in tqdm(range(len(q_lines))):
            q_lover = "Carol" in q_lines[i] or "守财奴" in q_lines[i]
            if q_lines[i].startswith('【禁用】'):
                if q_lover:
                    q_lines[i] = q_lines[i].replace('【禁用】', '')
                else:
                    continue
            if q_lover:
                continue
            try:
                q = q_lines[i].split('\t')[0].strip()
                a = q_lines[i].split('\t')[1].replace('\n', '').strip()
                perplexity, corrected_sent = perplexity_detection(a)
                has_error = grammar_analysis(a, nlp)
            except Exception as e:
                print(repr(e))
                q = q_lines[i]
                a = q
                corrected_sent = a
                has_error = True
                perplexity = True

            if perplexity or has_error:
                # print(i, q, a, '\n')
                # choice = input('是否删去？')
                choice = 'y'
                if choice == 'c':
                    q_lines[i] = q_lines[i].replace(a, corrected_sent)
                elif choice == 'y':
                    q_lines[i] = '【禁用】' + q_lines[i]
                elif choice == 'q':
                    break
            else:
                pass
        f_q.truncate(0)
        f_q.seek(0)
        f_q.writelines(q_lines)


def grammar_analysis(sentence, parser):
    try:
        segment, hidden = parser.seg([sentence])
    except Exception as e:
        print(repr(e))
        return True
    ner = parser.ner(hidden)
    # pos = parser.pos(hidden)
    srl = parser.srl(hidden)
    # dep = parser.dep(hidden)
    # sdp = parser.sdp(hidden)
    suspicion = srl[0].count([]) == len(segment[0])
    suspicion = len(ner[0]) != 0 or suspicion
    # suspicion = len(ner[0]) != 0
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
    corrected_sent = ""
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

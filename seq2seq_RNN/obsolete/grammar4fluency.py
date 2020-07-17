import pycorrector
from ltp import LTP
from tqdm import tqdm

from data.augmentation.blacklist import DFAFilter


def batch_mark():
    nlp = LTP()
    gfw = DFAFilter()
    gfw.parse('../augmentation/blacklist')
    pycorrector.enable_char_error(enable=False)
    corrected_sent, detail = pycorrector.correct("开始清洗")
    print(corrected_sent)
    text_path = "../data/resource/raw/all_corpus.tsv"
    with open(text_path, 'r+', encoding='utf-8-sig') as f_q:
        q_lines = f_q.readlines()
        for i in tqdm(range(20652, len(q_lines))):
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
                perplexity, corrected_sent = perplexity_detection([q, a])
                has_error = grammar_analysis([q, a], nlp)
                is_dirty = gfw.filter(q)[1]
                is_dirty = is_dirty or gfw.filter(a)[1]
            except Exception as e:
                print(repr(e))
                q = q_lines[i]
                a = q
                corrected_sent = [q, a]
                perplexity = True
                has_error = True
                is_dirty = True

            if perplexity or has_error or is_dirty:
                # print(i, q, a, '\n')
                # choice = input('是否删去？')
                choice = 'y'
                if choice == 'c':
                    q_lines[i] = q_lines[i].replace(a, corrected_sent[1])
                elif choice == 'y':
                    q_lines[i] = '【禁用】' + q_lines[i]
                elif choice == 'q':
                    break
            else:
                pass
            if i % 1000 == 0 and i != 0:
                f_q.truncate(0)
                f_q.seek(0)
                f_q.writelines(q_lines)
                print("checkpoint saved.")
        f_q.truncate(0)
        f_q.seek(0)
        f_q.writelines(q_lines)


def grammar_analysis(sentences, parser):
    suspicion = False
    for sentence in sentences:
        try:
            segment, hidden = parser.seg([sentence])
        except Exception as e:
            print(repr(e))
            return True
        ner = parser.ner(hidden)
        srl = parser.srl(hidden)
        suspicion = suspicion or (srl[0].count([]) == len(segment[0]))
        suspicion = suspicion or (len(ner[0]) != 0)
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
    detected = False
    corrected_sent_list = []
    for each in src:
        corrected_sent, detail = pycorrector.correct(each)
        detected = detected or (len(detail) != 0)
        corrected_sent_list.append(corrected_sent)
    # detected = False
    if detected:
        # print("detected")
        pass
    return detected, corrected_sent_list


def mark_invalid(invalid_indices, lines):
    for i in invalid_indices:
        lines[i] = "【禁用】" + lines[i]
    return lines


if __name__ == '__main__':
    batch_mark()

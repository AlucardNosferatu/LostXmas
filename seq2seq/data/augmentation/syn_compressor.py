import pickle
import synonyms
import numpy as np
from tqdm import tqdm


def getSynDict(freq_dist):
    syn_dict = {}
    for each in freq_dist[:800]:
        if len(each) >= 2:
            syn = synonyms.nearby(each)
            if len(syn[0]) <= 1:
                continue
            else:
                del syn[0][0]
                del syn[1][0]
                score = np.array(syn[1])
                syn = np.array(syn[0])
                syn = syn[np.where(score > 0.6)].tolist()
                if len(syn) < 3:
                    continue
                syn_dict[each] = syn
                print(syn)
    return syn_dict


def syn_replace():
    with open("../resource/raw/qingyun2.tsv", 'r', encoding='utf-8-sig') as f_o:
        last_index = len(f_o.readlines())
    f_o = open("../resource/raw/qingyun2.tsv", 'a', encoding='utf-8-sig')
    with open("../resource/raw/qingyun.tsv", 'r+', encoding='utf-8-sig') as f_r:
        raw_lines = f_r.readlines()
        backup_lines = raw_lines.copy()
    for i in tqdm(range(len(raw_lines))):
        raw_lines[i] = raw_lines[i].split('\t')[1].replace('\n', '').strip()
    replaced_lines = raw_lines.copy()
    with open('../resource/' + 'syn_dict.pkl', 'rb') as f_s:
        syn_dict = pickle.load(f_s, encoding='utf-8')
    for i in range(last_index, len(raw_lines)):
        line = raw_lines[i]
        rd = {}
        for key in syn_dict:
            result = filter(lambda syn: syn in line, syn_dict[key])
            result = list(result)
            if any(result):
                rd[result[0]] = rd.get(result[0], []) + [key]
        if any(rd):
            print()
            print(line)
            print(rd)
            print()
            if len(rd.keys()) == 1:
                r1 = "0"
            else:
                r1 = input("Replace?")
            if r1.isnumeric() and int(r1) <= len(rd.keys()) - 1:
                if len(rd[list(rd.keys())[int(r1)]]) == 1 and len(rd.keys()) > 1:
                    r2 = "0"
                else:
                    r2 = input("With?")
                if r2.isnumeric() and int(r2) <= len(rd[list(rd.keys())[int(r1)]]) - 1:
                    line = line.replace(list(rd.keys())[int(r1)], rd[list(rd.keys())[int(r1)]][int(r2)])
                    print(line)
        raw_lines[i] = line
        backup_lines[i] = backup_lines[i].replace(replaced_lines[i], raw_lines[i])
        f_o.write(backup_lines[i])
        f_o.flush()
    f_o.close()


def buildSynDict():
    with open('../resource/' + 'pad_word_to_index.pkl', 'rb') as f:
        word_to_index = pickle.load(f)
    word_to_index = list(word_to_index)
    SD = getSynDict(word_to_index)
    with open('../resource/' + 'syn_dict.pkl', 'wb') as f:
        pickle.dump(SD, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    # buildSynDict()
    syn_replace()

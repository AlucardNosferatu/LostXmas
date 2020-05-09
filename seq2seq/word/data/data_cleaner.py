from tqdm import tqdm
from snownlp import  SnowNLP


def filter_junk(raw_dialogs, output_path='test.txt'):
    ps = 'ps.txt'
    pollution_sign = open(ps, encoding='UTF-8-sig').read().split('\n')
    dialogs = open(raw_dialogs, encoding='UTF-8').read().split('\n')
    pairs = []
    for i in tqdm(range(0, len(dialogs), 2)):
        pairs.append([dialogs[i], dialogs[i + 1]])
    new_list = []
    for i in tqdm(range(0, len(pairs))):
        ban = False
        for sentence in pairs[i]:
            for sign in pollution_sign:
                if sign in sentence:
                    ban = True
                    break
            if ban:
                break
        if not ban:
            new_list.append(pairs[i][0])
            new_list.append(pairs[i][1])
    f = open(output_path, 'w+', encoding='UTF-8')
    f.write('\n'.join(new_list))
    f.close()
    return new_list


def auto_detect(raw_dialogs=None, dialogs=None, count=200, skip_detected=0, skip_lines=0):
    negative = []
    if dialogs is None:
        if raw_dialogs is None:
            print('give path of the file or input dialogs list as a parameter')
            return negative
        else:
            dialogs = open(raw_dialogs, encoding='UTF-8').read().split('\n')
    skipped = 0
    for i in tqdm(range(skip_lines, len(dialogs))):
        score = SnowNLP(dialogs[i]).sentiments
        if score < 0.1 and len(dialogs[i]) < 10:
            if skipped <= skip_detected:
                skipped += 1
            else:
                negative.append(str(i)+'   :'+dialogs[i])
                if len(negative) >= count:
                    break
    f = open('need to be checked.txt', 'w+', encoding='UTF-8')
    f.write('\n'.join(negative))
    f.close()
    return negative


filename = 'conv_zh.txt'
output = 'test.txt'
filter_junk(raw_dialogs=filename)
# auto_detect(raw_dialogs=output)

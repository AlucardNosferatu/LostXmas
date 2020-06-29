import os

import jieba
from tqdm import tqdm

from language.langconv import *


def Traditional2Simplified(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


def is_all_chinese(strs):
    for chart in strs:
        if chart < u'\u4e00' or chart > u'\u9fff':
            return False
    return True


def is_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
    return dir_list


def remove_brackets(lines):
    for i in tqdm(range(len(lines))):
        new_list = []
        temp = lines[i]
        if '[' in temp and ']' in temp and temp.index('[') < temp.index(']'):
            temp_list = temp.split('[')
            for each in temp_list:
                if ']' in each:
                    new_list += [each.split(']')[1]]
                else:
                    new_list += [each]
            temp_list = new_list
            lines[i] = " ".join(temp_list)
    return lines


def remove_banned(lines):
    i = 0
    while i < len(lines):
        temp = lines[i]
        if temp.startswith('【禁用】'):
            del lines[i]
        else:
            i += 1
    return lines


def append_extra_data(gfw, q_path, a_path, question, answer, filter_banned=True):
    skip_list = []
    with open(a_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        if filter_banned:
            lines = remove_banned(lines)
        for pos, line in enumerate(tqdm(lines)):
            a_filter = gfw.filter(line, '*')
            if a_filter[1]:
                skip_list.append(pos)
                continue
            else:
                answer.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    with open(q_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        if filter_banned:
            lines = remove_banned(lines)
        for pos, line in enumerate(tqdm(lines)):
            if pos in skip_list:
                continue
            else:
                question.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    assert len(question) == len(answer)
    return question, answer

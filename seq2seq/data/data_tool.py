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


def append_extra_data(q_path, a_path, question, answer):
    with open(q_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for pos, line in enumerate(tqdm(lines)):
            question.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    with open(a_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        for pos, line in enumerate(tqdm(lines)):
            answer.append(' '.join(jieba.lcut(Traditional2Simplified(line).strip(), cut_all=False)))
    return question, answer
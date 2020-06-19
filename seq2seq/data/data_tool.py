import os

from data.language.langconv import *


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

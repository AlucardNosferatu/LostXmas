import os

from ocr_config import text_dir, std_full_len
from ocr_util import ends_with_strs

import pycorrector


def correct_wrong_word(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        old = lines[i].split('\t')[1].strip('\n')
        tag = lines[i].split('\t')[0]
        new, _ = pycorrector.correct(old)
        lines[i] = tag + '\t' + new + '\n'
    with open(tgt_txt.replace('.txt', '_cor.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def manual_filter(tgt_txt, tag_missing=False):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if tag_missing:
        i = 0
        while i != len(lines):
            if i + 1 < len(lines):
                this_tag = lines[i].split('\t')[0]
                next_tag = lines[i + 1].split('\t')[0]
                if this_tag == next_tag:
                    insert_tag_missing = ''
                    while insert_tag_missing not in ['y', 'n']:
                        print('prev line:', lines[i].strip('\n'))
                        print('next line:', lines[i + 1].strip('\n'))
                        insert_tag_missing = input('y for tagging missing sentences\nn for pass')
                    if insert_tag_missing == 'y':
                        lines.insert(i + 1, 'm\t\n')
                i += 1
            else:
                break
    else:
        i = len(lines)
        while i != 0:
            i -= 1
            # do not check concatenated sentences
            if len(lines[i]) < std_full_len:
                drop_this_line = ''
                while drop_this_line not in ['y', 'n']:
                    print('Current txt:', tgt_txt)
                    if i - 1 >= 0:
                        print(lines[i - 1], lines[i])
                    else:
                        print(lines[i])
                    drop_this_line = input('y for drop\nn for pass')
                if drop_this_line == 'y':
                    lines.pop(i)

    with open(tgt_txt.replace('.txt', '_man.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def delete_redundant_version(txt_in_dir):
    for txt in txt_in_dir:
        old_txt = txt
        txt = txt.replace('.txt', '')
        txt = txt.split('_')
        last_mod = txt[-1]
        if txt.count(last_mod) > 1:
            rollback_ver = txt.index(last_mod)
            while len(txt) > rollback_ver + 1:
                txt.pop(-1)
            txt = '_'.join(txt)
            txt += '.txt'
            if os.path.exists(os.path.join(text_dir, txt)):
                os.remove(os.path.join(text_dir, txt))
            if os.path.exists(os.path.join(text_dir, old_txt)):
                os.rename(os.path.join(text_dir, old_txt), os.path.join(text_dir, txt))


if __name__ == '__main__':
    file_type_postfixes = [
        '_man.txt',
        '_fin.txt',
        '_rea.txt',
        '_cor.txt',
    ]
    skipped = [
        # 'xiaoice_island (1).txt',
        # 'xiaoice_island (2).txt',
        # 'xiaoice_island (3).txt',
        # 'xiaoice_island (4).txt',
        # 'xiaoice_island (5).txt',
        # 'xiaoice_island (6).txt',
        # 'xiaoice_island (7).txt',
        # 'xiaoice_island (8).txt',
        # 'xiaoice_island (9).txt',
        # 'xiaoice_island (10).txt',
        # 'xiaoice_island (11).txt',
        # 'xiaoice_island (12).txt',
        # 'xiaoice_island (13).txt',
        # 'xiaoice_island (14).txt',
        # 'xiaoice_island (15).txt',
        # 'xiaoice_island (16).txt',
        # 'xiaoice_island (17).txt',
    ]
    files = os.listdir(text_dir)
    delete_redundant_version(files)

    # # full-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         filter_by_prefix(os.path.join(text_dir, file))

    # # semi-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         concatenate_by_length_and_tag(os.path.join(text_dir, file))

    # # manual
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('_fin.txt') and file not in skipped:
    #         sort_by_batch(os.path.join(text_dir, file))

    # full-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
            correct_wrong_word(os.path.join(text_dir, file))

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('_cor.txt') and file not in skipped:
            manual_filter(os.path.join(text_dir, file), tag_missing=False)

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('_man.txt') and file not in skipped:
            manual_filter(os.path.join(text_dir, file), tag_missing=True)

    files = os.listdir(text_dir)
    delete_redundant_version(files)

    files = os.listdir(text_dir)
    delete_redundant_version(files)
    print('Done')

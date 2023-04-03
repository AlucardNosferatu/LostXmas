import os
import pycorrector

filter_prefixes = ['\n', '3月', '星期', '我滴老婆大人', '请使用文明用语']


def starts_with_strs(line, prefixes):
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False


def ends_with_strs(line, postfixes):
    for postfix in postfixes:
        if line.endswith(postfix):
            return True
    return False


def concatenate_unfinished(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    std_full_len = 10
    i = len(lines)
    while i != 0:
        i -= 1
        if i + 1 < len(lines) and len(lines[i]) >= std_full_len:
            finishe_with_nextline = ''
            while finishe_with_nextline not in ['y', 'n']:
                print(lines[i], lines[i + 1])
                finishe_with_nextline = input('y for finish this line with the next line\n n for skip')
            if finishe_with_nextline == 'y':
                next_line = lines.pop(i + 1)
                lines[i] = lines[i].strip('\n')
                lines[i] += next_line
    with open(tgt_txt.replace('.txt', '_fin.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def filter_one_txt(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    i = len(lines)
    while i != 0:
        i -= 1
        drop = False
        if starts_with_strs(lines[i], filter_prefixes):
            drop = True
        if drop:
            lines.pop(i)
    with open(tgt_txt.replace('.txt', '_fil.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def rearrange_sequence(tgt_txt):
    window_size = 5
    index_str_list = [str(index) for index in list(range(5))]

    def format_error(arr_str):
        for index_str in index_str_list:
            if index_str not in arr_str:
                return True
        return False

    def arr_str_process(arr_str):
        arr_str = list(arr_str)
        arr_size = len(arr_str)
        for k in range(arr_size):
            backward_i = arr_size - k - 1
            if arr_str[backward_i] not in index_str_list:
                arr_str.pop(backward_i)
            elif arr_str[backward_i] in arr_str[:backward_i]:
                arr_str.pop(backward_i)
        ''.join(arr_str)
        return arr_str

    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines) - window_size + 1):
        seq_batch = lines[i:i + window_size].copy()
        arrangement = 'bruh'
        while arrangement != '' and format_error(arrangement):
            print(''.join(seq_batch))
            arrangement = input('input rearranged order index, start from 0')
        if arrangement == '':
            continue
        else:
            arrangement = arr_str_process(arrangement)
            rearr_seq_batch = seq_batch.copy()
            for j in range(window_size):
                rearr_seq_batch[j] = seq_batch[int(arrangement[j])]
            lines[i:i + window_size] = rearr_seq_batch
    with open(tgt_txt.replace('.txt', '_rea.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def correct_wrong_word(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        corrected_sent, _ = pycorrector.correct(lines[i])
        lines[i] = corrected_sent
    with open(tgt_txt.replace('.txt', '_cor.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def manual_filter(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    i = len(lines)
    while i != 0:
        i -= 1
        drop_this_line = ''
        while drop_this_line not in ['y', 'n']:
            if i - 1 >= 0:
                print(lines[i - 1], lines[i])
            else:
                print(lines[i])
            drop_this_line = input('y for drop\nn for pass')
        if drop_this_line == 'y':
            lines.pop(i)
    with open(tgt_txt.replace('.txt', '_man.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def tag_q_or_a(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        q_or_a = ''
        while q_or_a not in ['q', 'a']:
            if i + 1 < len(lines):
                print(lines[i], lines[i + 1])
            else:
                print(lines[i])
            q_or_a = input('q for question\na for answer')
        lines[i] = q_or_a + '\t' + lines[i]
    with open(tgt_txt.replace('.txt', '_tag.txt'), 'w', encoding='utf-8') as f:
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
            if os.path.exists(os.path.join('texts', txt)):
                os.remove(os.path.join('texts', txt))
            if os.path.exists(os.path.join('texts', old_txt)):
                os.rename(os.path.join('texts', old_txt), os.path.join('texts', txt))


if __name__ == '__main__':
    file_type_postfixes = ['_fil.txt', '_fin.txt', '_fin.txt', '_rea.txt', '_cor.txt']
    skipped = [
        'xiaoice_island (1)_fil_fin_man.txt',
        'xiaoice_island (10)_fil_fin_man.txt'
    ]
    files = os.listdir('texts')
    delete_redundant_version(files)
    # files = os.listdir('texts')
    # for file in files:
    #     if not ends_with_strs(file, file_type_postfixes) and file not in skipped:
    #         filter_one_txt(os.path.join('texts', file))
    # files = os.listdir('texts')
    # for file in files:
    #     if file.endswith('_fil.txt') and file not in skipped:
    #         concatenate_unfinished(os.path.join('texts', file))
    # files = os.listdir('texts')
    # for file in files:
    #     if file.endswith('_fin.txt') and file not in skipped:
    #         manual_filter(os.path.join('texts', file))
    files = os.listdir('texts')
    for file in files:
        if file.endswith('_man.txt') and file not in skipped:
            tag_q_or_a(os.path.join('texts', file))
    files = os.listdir('texts')
    for file in files:
        if file.endswith('_tag.txt') and file not in skipped:
            rearrange_sequence(os.path.join('texts', file))
    files = os.listdir('texts')
    for file in files:
        if file.endswith('_rea.txt') and file not in skipped:
            correct_wrong_word(os.path.join('texts', file))
    files = os.listdir('texts')
    delete_redundant_version(files)
    print('Done')

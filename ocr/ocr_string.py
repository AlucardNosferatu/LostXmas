import os
import pycorrector

filter_prefixes = ['\n', '3月', '星期', '我滴老婆大人', '请使用文明用语']


def concatenate_unfinished(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    std_full_len = 12
    i = len(lines)
    while i != 0:
        i -= 1
        if i + 1 < len(lines) and len(lines[i]) >= std_full_len:
            finishe_with_nextline = ''
            while finishe_with_nextline not in ['y', 'n']:
                print(lines[i], lines[i + 1])
                finishe_with_nextline = input('y/n')
            if finishe_with_nextline == 'y':
                next_line = lines.pop(i + 1)
                lines[i] = lines[i].strip('\n')
                lines[i] += next_line
    with open(tgt_txt.replace('.txt', '_fin.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


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


if __name__ == '__main__':
    file_type_postfixes = ['_fil.txt', '_fin.txt', '_fin.txt', '_rea.txt', '_cor.txt']
    # files = os.listdir('texts')
    # for file in files:
    #     if not ends_with_strs(file, file_type_postfixes):
    #         filter_one_txt(os.path.join('texts', file))
    # files = os.listdir('texts')
    # for file in files:
    #     if file.endswith('_fil.txt'):
    #         concatenate_unfinished(os.path.join('texts', file))
    files = os.listdir('texts')
    for file in files:
        if file.endswith('_fin.txt'):
            rearrange_sequence(os.path.join('texts', file))
    files = os.listdir('texts')
    for file in files:
        if file.endswith('_rea.txt'):
            correct_wrong_word(os.path.join('texts', file))
    print('Done')

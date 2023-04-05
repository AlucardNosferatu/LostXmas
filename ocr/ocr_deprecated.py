from ocr import filter_prefixes
from ocr_config import std_full_len
from ocr_util import starts_with_strs


def manual_tag(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        q_or_a = ''
        while q_or_a not in ['q', 'a']:
            print('Current txt:', tgt_txt)
            if i + 1 < len(lines):
                print(lines[i], lines[i + 1])
            else:
                print(lines[i])
            q_or_a = input('q for question\na for answer')
        lines[i] = q_or_a + '\t' + lines[i]
    with open(tgt_txt.replace('.txt', '_tag.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def concatenate_by_length_and_tag(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = len(lines)
    while i != 0:
        i -= 1
        if i + 1 < len(lines):
            detected = False
            tag = lines[i].split('\t')[0]
            tag_next = lines[i + 1].split('\t')[0]
            if len(lines[i]) >= std_full_len and tag == tag_next:
                detected = True
            if detected:
                finishe_with_nextline = ''
                while finishe_with_nextline not in ['y', 'n']:
                    print('Current txt:', tgt_txt)
                    print(lines[i], lines[i + 1])
                    finishe_with_nextline = input('y for finish this line with the next line\n n for skip')
                if finishe_with_nextline == 'y':
                    next_line = lines.pop(i + 1)
                    lines[i] = lines[i].strip('\n')
                    lines[i] += next_line.split('\t')[1]
    with open(tgt_txt.replace('.txt', '_fin.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


def sort_by_batch(tgt_txt):
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
            print('Current txt:', tgt_txt)
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


def filter_by_prefix(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    i = len(lines)
    while i != 0:
        i -= 1
        drop = False
        if starts_with_strs(lines[i].split('\t')[1], filter_prefixes):
            drop = True
        if drop:
            lines.pop(i)
    with open(tgt_txt, 'w', encoding='utf-8') as f:
        f.writelines(lines)

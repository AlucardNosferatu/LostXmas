import os

# import pycorrector

text_dir = 'texts'
filter_prefixes = ['\n', '3月', '星期', '我滴老婆大人', '请使用文明用语']
std_full_len = 10


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


# def correct_wrong_word(tgt_txt):
#     with open(tgt_txt, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#     for i in range(len(lines)):
#         corrected_sent, _ = pycorrector.correct(lines[i])
#         lines[i] = corrected_sent
#     with open(tgt_txt.replace('.txt', '_cor.txt'), 'w', encoding='utf-8') as f:
#         f.writelines(lines)


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


if __name__ == '__main__':
    file_type_postfixes = [
        '_man.txt',
        '_fin.txt',
        '_rea.txt',
        '_cor.txt',
    ]
    skipped = [
        'xiaoice_island (1).txt',
        'xiaoice_island (10).txt',
        'xiaoice_island (11).txt',
        'xiaoice_island (12).txt'
    ]
    files = os.listdir(text_dir)
    delete_redundant_version(files)

    # full-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
            filter_by_prefix(os.path.join(text_dir, file))

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes) and file not in skipped:
            concatenate_unfinished(os.path.join(text_dir, file))

    # manual
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('_fin.txt') and file not in skipped:
            rearrange_sequence(os.path.join(text_dir, file))

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('_rea.txt') and file not in skipped:
            manual_filter(os.path.join(text_dir, file), tag_missing=False)

    # semi-auto
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('_man.txt') and file not in skipped:
            manual_filter(os.path.join(text_dir, file), tag_missing=True)

    files = os.listdir(text_dir)
    delete_redundant_version(files)

    # full-auto
    # files = os.listdir(text_dir)
    # for file in files:
    #     if file.endswith('_man.txt') and file not in skipped:
    #         correct_wrong_word(os.path.join(text_dir, file))

    files = os.listdir(text_dir)
    delete_redundant_version(files)
    print('Done')

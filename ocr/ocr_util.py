import os.path

from ocr_config import file_type_postfixes, text_dir


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


def calculate_filter_ratio(tgt_txt):
    with open(tgt_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if os.path.exists(tgt_txt.replace('.txt', '_mat.txt')):
        with open(tgt_txt.replace('.txt', '_mat.txt'), 'r', encoding='utf-8') as f:
            mat_lines = f.readlines()
    elif os.path.exists(tgt_txt.replace('.txt', '_eag_mat.txt')):
        with open(tgt_txt.replace('.txt', '_eag_mat.txt'), 'r', encoding='utf-8') as f:
            mat_lines = f.readlines()
    else:
        mat_lines = []

    filtered = []
    ratio = len(mat_lines) / len(lines)
    for line in lines:
        if line not in mat_lines:
            filtered.append(line)

    with open(tgt_txt.replace('.txt', '_fil.txt'), 'w', encoding='utf-8') as f:
        f.writelines(filtered)
    print(tgt_txt, ':', ratio)


if __name__ == '__main__':
    files = os.listdir(text_dir)
    for file in files:
        if file.endswith('.txt') and not ends_with_strs(file, file_type_postfixes):
            calculate_filter_ratio(os.path.join(text_dir, file))

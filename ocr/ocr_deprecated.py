from ocr_string import starts_with_strs

filter_prefixes = ['\n', '3月', '星期', '我滴老婆大人', '请使用文明用语']


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
    with open(tgt_txt.replace('.txt', '_fil.txt'), 'w', encoding='utf-8') as f:
        f.writelines(lines)


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

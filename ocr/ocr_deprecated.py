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

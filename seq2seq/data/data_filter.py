def manual_filter():
    with open('resource/raw/qingyun.tsv', 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        lines = lines[:-2]
    f = open('resource/raw/legacy/question.txt', 'a', encoding='utf-8')
    f1 = open('resource/raw/legacy/answer.txt', 'a', encoding='utf-8')
    i = 0
    while i < len(lines):
        line = lines[i]
        if '\t' not in line:
            print(line)
        line = line.split('\t')
        q = line[0].strip() + "\n"
        a = line[1].strip() + "\n"
        print("问：", q)
        print("答：", a)
        p = input("是否合格？")
        if p == "n":
            del lines[i]
        elif p == "y":
            f.write(q)
            f1.write(a)
            f.flush()
            f1.flush()
            i += 1
        else:
            print("y for pass, n for fail")
    f.close()
    f1.close()


manual_filter()

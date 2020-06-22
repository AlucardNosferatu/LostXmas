from data.augmentation.blacklist import DFAFilter, NaiveFilter, BSFilter


def prompt_filter(show_ng=True):
    gfw = DFAFilter()
    gfw.parse("keywords")
    with open('../resource/raw/qingyun.tsv', 'r', encoding='utf-8-sig') as q_f:
        lines = q_f.read().split('\n')
        lines = lines[:-2]
    q_f = open('../resource/raw/legacy/question.txt', 'a', encoding='utf-8-sig')
    a_f = open('../resource/raw/legacy/answer.txt', 'a', encoding='utf-8-sig')
    i = 0
    while i < len(lines):
        line = lines[i]
        if '\t' not in line:
            print(line)
        is_ng = gfw.filter(line, '*')
        if not (show_ng ^ is_ng[1]):
            print(line)
            line = is_ng[0].split('\t')
            q = line[0].strip() + "\n"
            a = line[1].strip() + "\n"
            print("问：", q)
            print("答：", a)
            p = input("是否合格？\n输入y为合格\n输入n为不合格\n输入1为没听懂\n输入1为不认识")
            if p == "n":
                del lines[i]
            elif p == "y":
                q_f.write(q)
                a_f.write(a)
                q_f.flush()
                a_f.flush()
                i += 1
            elif p == "1":
                q_f.write(q)
                a = "啥。。。没明白\n"
                a_f.write(a)
                q_f.flush()
                a_f.flush()
                i += 1
            elif p == "2":
                q_f.write(q)
                a = "不认识。。。你说的是谁？\n"
                a_f.write(a)
                q_f.flush()
                a_f.flush()
                i += 1
            else:
                print("y for pass, n for fail")
        else:
            del lines[i]
    q_f.close()
    a_f.close()


if __name__ == "__main__":
    prompt_filter()

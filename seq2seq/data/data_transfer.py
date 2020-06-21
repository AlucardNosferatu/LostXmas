from tqdm import tqdm


def manual_filter():
    with open('resource/raw/legacy/conv_zh.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    question = lines[::2]
    answer = lines[1::2]
    i = 0
    f = open('resource/raw/legacy/question.txt', 'a', encoding='utf-8')
    f1 = open('resource/raw/legacy/answer.txt', 'a', encoding='utf-8')
    while i < len(question):
        print("问：", question[i])
        print("答：", answer[i])
        if (input("是否合格？")) == "n":
            del question[i]
            del answer[i]
        else:
            f.write(question[i])
            f1.write(answer[i])
            f.flush()
            f1.flush()
            i += 1
    f.close()
    f1.close()


def line_filter(lines):
    for i in tqdm(range(len(lines))):
        new_list = []
        temp = lines[i]
        temp_list = temp.split('[')
        for each in temp_list:
            if ']' in each:
                new_list += [each.split(']')[1]]
            else:
                new_list += [each]
        temp_list = new_list
        lines[i] = " ".join(temp_list)
    return lines


def batch_filter():
    with open('resource/raw/legacy/answer.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = line_filter(lines)
    with open('resource/raw/legacy/answer.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)


# batch_filter()

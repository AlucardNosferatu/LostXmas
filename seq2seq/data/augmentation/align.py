from tqdm import tqdm


def split_continuous_speech():
    f = open('../resource/raw/legacy/unsorted/CPoL4OC.txt', 'r', encoding='utf-8-sig')
    q_out = open('../resource/raw/legacy/unsorted/CPoL4OC_Q.txt', 'a', encoding='utf-8-sig')
    a_out = open('../resource/raw/legacy/unsorted/CPoL4OC_A.txt', 'a', encoding='utf-8-sig')
    sentences = f.readlines()
    f.close()
    i = 0
    while i < (len(sentences) - 1):
        q = sentences[i]
        a_list = []
        print("", q)

        for j in range(i + 1, i + 5):
            a_list.append(sentences[j])
        print("", a_list)
        answer_index = input("which answer?")
        if answer_index.isnumeric():
            a = a_list[int(answer_index)]
        else:
            continue

        choice = input("?")
        if choice == 'r':
            i -= 1
            if i < 0:
                i = 0
        elif choice == 'y':
            q_out.write(q)
            q_out.flush()
            a_out.write(a)
            a_out.flush()
            i += 1
        elif choice == 'n' or choice == '0':
            i += 1
        elif choice == 'cq':
            sentences[i + 1] = q.replace('\n', '') + a
            i += 1
        elif choice == 'ca':
            answer_index = input("another answer?")
            if answer_index.isnumeric():
                a = a.replace('\n', '') + a_list[int(answer_index)]
                q_out.write(q)
                q_out.flush()
                a_out.write(a)
                a_out.flush()
                i += 1
        elif choice == 's':
            q_or_a = input("Q or A?")
            if q_or_a == 'q':
                temp = sentences[i]
                q_or_a = i
            elif q_or_a == 'a':
                temp = sentences[i + 1]
                q_or_a = i + 1
            else:
                continue
            temp = temp.replace(
                ',', '#$%'
            ).replace(
                '，', '#$%'
            ).replace(
                '.', '#$%'
            ).replace(
                '。', '#$%'
            ).replace(
                ' ', '#$%'
            ).replace(
                '！', '#$%'
            ).replace(
                '？', '#$%'
            ).replace(
                '!', '#$%'
            ).replace(
                '?', '#$%'
            ).split('#$%')
            print(temp)
            left_sen = input("which sentence?")
            if left_sen.isnumeric():
                print(temp[int(left_sen)])
                sentences[q_or_a] = temp[int(left_sen)]
        else:
            pass
    q_out.close()
    a_out.close()


def set_QA(lines, i, gfw, show_ng):
    q = lines[i]
    a_list = []
    print("", q)
    j = i + 1
    while len(a_list) < 6:
        is_ng = gfw.filter(lines[j], '*')
        if not (show_ng ^ is_ng[1]):
            a_list.append(lines[j])
        j += 1
    print("", a_list)
    answer_index = input("which answer?")
    if answer_index.isnumeric():
        a = a_list[int(answer_index)]
    else:
        a = None
    return q, a


def concat(choice, sentences, i, input_a, gfw, show_ng):
    if choice == 'cq':
        q = sentences[i]
        sentences[i] = q.replace('\n', '') + input_a
    elif choice == 'ca':
        a_list = []
        j = i + 1
        while len(a_list) < 6:
            is_ng = gfw.filter(sentences[j], '*')
            if not (show_ng ^ is_ng[1]):
                a_list.append(sentences[j])
            j += 1
        print(a_list)
        answer_index = input("another answer?")
        if answer_index.isnumeric():
            if int(answer_index) < len(a_list):
                sentences[int(answer_index) + i + 1] = input_a.replace('\n', '') + a_list[int(answer_index)]
            else:
                # ca时选项是数字但超出a_list范围
                pass
        else:
            # ca时选项不是数字
            pass
    else:
        # 不符合cq或ca
        pass
    return sentences, i


if __name__ == "__main__":
    split_continuous_speech()

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
        elif choice == 'c':
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


if __name__ == "__main__":
    split_continuous_speech()

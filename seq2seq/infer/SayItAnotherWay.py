from nlpcda import Randomword, Similarword


def get_siaw(sentence, smw):
    sentence = sentence.replace('\n', '')
    rs1 = [sentence]
    for each in smw:
        length = len(rs1)
        for i in range(length):
            rs1 += each.replace(rs1[i])
    rs1 = list(set(rs1))
    return rs1


def use_log():
    f_q = open("Online_Q.txt", 'r+', encoding='utf-8-sig')
    f_a = open("Online_A.txt", 'r+', encoding='utf-8-sig')
    # f_q = open("../data/resource/raw/legacy/ChatterBot_Q.txt", 'r+', encoding='utf-8-sig')
    # f_a = open("../data/resource/raw/legacy/ChatterBot_A.txt", 'r+', encoding='utf-8-sig')
    q_lines = f_q.readlines()
    a_lines = f_a.readlines()
    new_q = []
    new_a = []
    smw = [Randomword(create_num=5, change_rate=0.3)]
    smw += [Similarword(create_num=5, change_rate=0.3)]
    for i in range(len(q_lines)):
        q_list = get_siaw(q_lines[i], smw)
        a_list = get_siaw(a_lines[i], smw)
        q_list = q_list[:min(len(q_list), len(a_list))]
        a_list = a_list[:min(len(q_list), len(a_list))]
        new_q += q_list
        new_a += a_list
    assert len(new_a) == len(new_q)
    for i in range(len(new_q)):
        new_q[i] += '\n'
        new_a[i] += '\n'
    f_q.truncate(0)
    f_a.truncate(0)
    f_q.seek(0)
    f_a.seek(0)
    f_q.writelines(new_q)
    f_a.writelines(new_a)


if __name__ == '__main__':
    use_log()

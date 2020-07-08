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


def use_log(base_dir="../"):
    with open(base_dir + "infer/Online_Q.txt", 'r', encoding='utf-8-sig') as f_q:
        q_lines = f_q.readlines()
    with open(base_dir + "infer/Online_A.txt", 'r', encoding='utf-8-sig') as f_a:
        a_lines = f_a.readlines()
    # new_q = q_lines.copy()
    # new_a = a_lines.copy()
    new_q = []
    new_a = []
    smw = [Randomword(create_num=5, change_rate=0.05)]
    smw += [Similarword(create_num=5, change_rate=0.05)]
    for i in range(len(q_lines)):
        q_list = get_siaw(q_lines[i], smw)
        # a_list = get_siaw(a_lines[i], smw)
        a_list = [a_lines[i]] * len(q_list)
        # q_list = q_list[:min(len(q_list), len(a_list))]
        # a_list = a_list[:min(len(q_list), len(a_list))]
        new_q += q_list
        new_a += a_list
    assert len(new_a) == len(new_q)
    for i in range(len(new_q)):
        new_q[i] = new_q[i].replace('\n', '')
        new_a[i] = new_a[i].replace('\n', '')
        new_q[i] += '\n'
        new_a[i] += '\n'
    with open(base_dir + "infer/Online_Q_SIAW.txt", 'w', encoding='utf-8-sig') as f_q:
        f_q.writelines(new_q)
    with open(base_dir + "infer/Online_A_SIAW.txt", 'w', encoding='utf-8-sig') as f_a:
        f_a.writelines(new_a)


if __name__ == '__main__':
    use_log()

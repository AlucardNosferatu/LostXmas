f = open("Lovers.txt", 'r', encoding='utf-8-sig')
lines = f.readlines()
f.close()
q = lines[::2]
a = lines[1::2]
q_f = open("../Lovers_Q.txt", 'a', encoding='utf-8-sig')
a_f = open("../Lovers_A.txt", 'a', encoding='utf-8-sig')
q_f.writelines(q)
a_f.writelines(a)
q_f.flush()
a_f.flush()
q_f.close()
a_f.close()

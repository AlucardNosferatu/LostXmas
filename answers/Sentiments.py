from snownlp import SnowNLP
f=open("Answers.txt")
Answers=f.read().split('\n')
f.close()

for each in Answers:
    s = SnowNLP(each)
    print(str(s.sentiments))

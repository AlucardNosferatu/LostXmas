from snownlp import SnowNLP


def fromStr(str):

    s_object = SnowNLP(str)

    score = 1-s_object.sentiments
    
    f=open("answers\Answers.txt")
    Answers=f.read().split('\n')
    f.close()

    Scores=[]
    for each in Answers:
        Scores.append(SnowNLP(each).sentiments)

    for index in range(1,len(Scores)):
        if score<Scores[index]:
            return Answers[index-1]

    return "你高兴就好~"

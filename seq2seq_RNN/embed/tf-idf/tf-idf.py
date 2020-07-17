import jieba
from sklearn.feature_extraction.text import TfidfVectorizer


def cut_words():
    con1 = jieba.cut("今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。")

    con2 = jieba.cut("我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。")

    con3 = jieba.cut("如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。")
    c1 = " ".join(con1)
    c2 = " ".join(con2)
    c3 = " ".join(con3)

    return c1, c2, c3


def tf_idf():
    """
    中文特征化
    :return None
    """
    c1, c2, c3 = cut_words()
    print("c1:", c1)
    tf = TfidfVectorizer()
    data = tf.fit_transform([c1, c2, c3])
    print("特征：")
    print(tf.get_feature_names())
    print("特征的大小：")
    print(len(tf.get_feature_names()))
    print("词向量：")
    print(data.toarray())
    print("第一列词向量的个数:")
    print(len(data.toarray()[0]))
    return None


tf_idf()

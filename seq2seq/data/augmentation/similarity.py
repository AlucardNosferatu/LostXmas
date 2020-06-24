from math import sqrt
from snownlp import SnowNLP
import distance
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer


def Keywords_IoU(s1, s2):
    s1 = SnowNLP(s1)
    s2 = SnowNLP(s2)
    s1 = s1.keywords()
    s2 = s2.keywords()
    s1 = set(s1)
    s2 = set(s2)
    intersection = s1.intersection(s2)
    union = s1.union(s2)
    intersection = list(intersection)
    union = list(union)
    IoU = len(intersection) / len(union)
    return IoU, len(intersection)


def LongSubString(s1, s2):
    """
    查找两个字符串中相同的最大字串
    使用了滑动窗口的思想
    """
    MaxLength = 0  # 记录当前字串最大长度
    MaxString = ''  # 记录当前最大字串
    new1 = ''  # 第一个字符串的拼接子串
    for v1 in s1:
        new1 += v1
        new2 = ''  # 第二个字符串的拼接子串
        for v2 in s2:
            new2 += v2
            while len(new2) > len(new1):
                # 当第二个字串的长度大于第一个字串时，则从第二个子串的第一个字符开始删除，直到两个子串长度相等
                new2 = new2[1:]
            if new2 == new1 and len(new2) > MaxLength:
                # 当两个子串的内容相等且长度大于当前最大长度时就记录当前字符串并更新最大长度
                MaxLength = len(new2)
                MaxString = new2
        if MaxString != new1:
            # 内层循环完成后比较外层的子串与最大子串内容是否相同，不同时从外层子串的第一个字符开始删除
            new1 = new1[1:]
    return MaxString, MaxLength


def edit_distance(s1, s2):
    score = 1 - (distance.levenshtein(s1, s2) / max(len(s1), len(s2)))
    return score


def jaccard_improved(s1, s2):
    if (s1 in s2 and len(s1) > 5) or (s2 in s1 and len(s2) > 5):
        return 1
    else:
        _, overlapped_length = LongSubString(s1, s2)
        score = overlapped_length / (((len(s1) + len(s2)) / 2) - overlapped_length)
        score = sqrt(score)
        return score


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator / denominator


def tf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))


def similarity_complex(s1, s2):
    # score1 = jaccard_similarity(s1, s2)
    score1 = jaccard_improved(s1, s2)
    score2 = edit_distance(s1, s2)
    score3 = tf_similarity(s1, s2)
    mean_score = np.mean(np.array([score1, score2, score3]))
    max_score = np.max(np.array([score1, score2, score3]))
    std_score = np.std(np.array([score1, score2, score3]))
    # print("杰卡德距离：", score1)
    # print("编辑相似性：", score2)
    # print("余弦相似性：", score3)
    # print("平均值：", mean_score)
    # print("最大值：", max_score)
    # print("标准差：", std_score)
    return [score1, score2, score3], mean_score, max_score, std_score


if __name__ == '__main__':
    sa = "早上好啊现在是最爱的了"
    sb = "早上好啊，现在是16点36分，吃早餐了吗"
    # score1 = jaccard_similarity(s1, s2)
    score1 = jaccard_improved(sa, sb)
    score2 = edit_distance(sa, sb)
    score3 = tf_similarity(sa, sb)
    score4, _ = Keywords_IoU(sa, sb)
    mean_score = np.mean(np.array([score1, score2, score3]))
    max_score = np.max(np.array([score1, score2, score3]))
    std_score = np.std(np.array([score1, score2, score3]))
    print("杰卡德距离：", score1)
    print("编辑相似性：", score2)
    print("余弦相似性：", score3)
    print("关键词比例：", score4)
    print("平均值：", mean_score)
    print("最大值：", max_score)
    print("标准差：", std_score)

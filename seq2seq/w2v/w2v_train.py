import logging
import multiprocessing
import os.path
import sys
import warnings

import gensim
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from tqdm import tqdm

filePath = 'corpus_1.txt'
fileSegWordDonePath = 'corpusSegDone_1.txt'
inp = 'corpusSegDone_1.txt'
out_model = 'corpusSegDone_1.model'
out_vector = 'corpusSegDone_1.vector'


# 打印中文列表
def print_list_chinese(input_list):
    for i in range(len(input_list)):
        print(input_list[i])

    # 读取文件内容到列表


def process_raw(file_path):
    file_train_read = []
    with open(file_path, mode='r', encoding='utf-8-sig') as fileTrainRaw:
        for line in fileTrainRaw:  # 按行读取文件
            file_train_read.append(line)
    return file_train_read


# jieba分词后保存在列表中
def tokenize_and_save(file_train_read):
    file_train_seg = []
    for i in tqdm(range(len(file_train_read))):
        file_train_seg.append([' '.join(list(jieba.cut(file_train_read[i], cut_all=False)))])
    # 保存分词结果到文件中
    with open(fileSegWordDonePath, 'w', encoding='utf-8') as fW:
        for i in tqdm(range(len(file_train_seg))):
            fW.write(file_train_seg[i][0])
            fW.write('\n')


"""
gensim word2vec获取词向量
"""


def incremental_train(more_sentences, base_dir="../"):
    model_w2v = gensim.models.Word2Vec.load(base_dir + "w2v/" + out_model)
    model_w2v.build_vocab(more_sentences, update=True)
    model_w2v.train(more_sentences, total_examples=model_w2v.corpus_count, epochs=model_w2v.iter)
    # 保存模型
    model_w2v.save(base_dir + "w2v/" + out_model)
    # 保存词向量
    model_w2v.wv.save_word2vec_format(base_dir + "w2v/" + out_vector, binary=False)


def initial_train():
    ftr = process_raw(filePath)
    tokenize_and_save(ftr)
    program = os.path.basename(sys.argv[0])  # 读取当前文件的文件名
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # inp为输入语料, outp1为输出模型, outp2为vector格式的模型

    # 训练skip-gram模型
    model = Word2Vec(LineSentence(inp), size=50, window=5, min_count=5,
                     workers=multiprocessing.cpu_count())

    # 保存模型
    model.save(out_model)
    # 保存词向量
    model.wv.save_word2vec_format(out_vector, binary=False)


# 忽略警告
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

if __name__ == '__main__':
    initial_train()

import pickle

import jieba

from train.utils import load_resource


def input_question(seq="还须努力", BaseDir='../'):
    _, _, _, _, word_to_index, _ = load_resource(BaseDir=BaseDir)
    with open(BaseDir + 'data/resource/composable.pkl', 'rb') as f:
        all_composed = pickle.load(f)
    with open(BaseDir + 'data/resource/syn_dict.pkl', 'rb') as f:
        syn = pickle.load(f)
    seq = seq.replace('，', ',').replace('。', '.')
    seq = jieba.lcut(seq.strip(), cut_all=False)
    for k in range(len(seq)):
        if not seq[k] in word_to_index:
            print(seq[k])



if __name__ == '__main__':
    input_question()
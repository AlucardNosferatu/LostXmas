import torch
from torch import cosine_similarity
from torch.nn import functional as F


def similarity_slow(vec1, vec2):
    token_count = vec1.shape[0]
    cs_matrix = torch.zeros(token_count, token_count, dtype=torch.float32)
    for i in range(token_count):
        for j in range(token_count):
            cs_matrix[i, j] = cosine_similarity(x1=vec1[i, :, :], x2=vec2[j, :, :]).item()
    cs_score = cs_matrix.sum() / (token_count * token_count)
    return cs_score, cs_matrix


def similarity(vec1, vec2=None, pad_mask=None):
    # 归一化向量（按最后一个维度L2归一化）
    vec1_2d = vec1.squeeze(1)
    vec2_2d = vec2.squeeze(1)
    if pad_mask is not None:
        vec1_pad_after = pad_mask[0]
        vec2_pad_after = pad_mask[1]
        vec1_2d = vec1_2d[:vec1_pad_after, :]
        vec2_2d = vec2_2d[:vec2_pad_after, :]
    norm_vec1 = F.normalize(vec1_2d, p=2, dim=-1)
    if vec2 is None:
        norm_vec2 = norm_vec1
    else:
        norm_vec2 = F.normalize(vec2_2d, p=2, dim=-1)
    # 计算余弦相似度矩阵（向量化操作）
    similarity_matrix = torch.mm(norm_vec1, norm_vec2.T)
    # 计算平均相似度
    cs_score = similarity_matrix.mean()
    return cs_score, similarity_matrix

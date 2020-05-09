import numpy as np
import tensorflow as tf
from tqdm import tqdm
from text_clustering.distance import euc_distance, load_sentences, sen2vec, vec_wrapper


def loader(count=20):
    lines, idx_map = load_sentences()
    sen_vec = sen2vec(input_id_map=idx_map, input_lines=lines, count=count, pad=True)
    new_vec = []
    for each in sen_vec:
        new_vec.append(np.array(each[1]))
    output_array = np.array(new_vec)
    return output_array, idx_map, sen_vec


def rand_cent(data_set, k):  # 第一个中心点初始化
    n = np.shape(data_set)[1]
    centroids_matrix = np.mat(np.zeros([k, n]))  # 创建 k 行 n列的全为0 的矩阵
    for j in range(n):
        minj = np.min(data_set[:, j])  # 获得第j 列的最小值
        rangej = float(np.max(data_set[:, j]) - minj)  # 得到最大值与最小值之间的范围
        # 获得输出为 K 行 1 列的数据，并且使其在数据集范围内
        centroids_matrix[:, j] = np.mat(minj + rangej * np.random.rand(k, 1))
    return centroids_matrix


def k_means(w2idx, data_set, k, dist_means=euc_distance, create_cent=rand_cent):
    m = np.shape(data_set)[0]  # 得到行数，即为样本数
    cluster_assessment = np.mat(np.zeros([m, 2]))  # 创建 m 行 2 列的矩阵
    cent = create_cent(data_set, k)  # 初始化 k 个中心点
    cluster_changed = True
    sess = tf.InteractiveSession()
    while cluster_changed:
        cluster_changed = False
        for index in range(m):
            min_dist = np.inf  # 初始设置值为无穷大
            min_index = -1
            print(index)
            for j in tqdm(range(k)):
                #  j循环，先计算 k个中心点到1 个样本的距离，在进行i循环，计算得到k个中心点到全部样本点的距离
                cent_tensor = vec_wrapper(cent[j, :].transpose())
                comp_tensor = vec_wrapper(data_set[index, :])
                dist1, dist2 = dist_means(cent_tensor, comp_tensor, w2idx, pad=False)
                # dist_j = dist1.eval()[0]
                dist_j = sess.run(dist1)
                if dist_j < min_dist:
                    min_dist = dist_j  # 更新 最小的距离
                    min_index = j
            if cluster_assessment[index, 0] != min_index:  # 如果中心点不变化的时候， 则终止循环
                cluster_changed = True
            cluster_assessment[index, :] = min_index, min_dist ** 2  # 将 index，k值中心点 和  最小距离存入到数组中
        # print(centroids)

        # 更换中心点的位置
        for cent in range(k):
            pts_in_cluster = data_set[np.nonzero(cluster_assessment[:, 0].A == cent)[0]]  # 分别找到属于k类的数据
            if len(pts_in_cluster) != 0:
                cent[cent, :] = np.mean(pts_in_cluster, axis=0)  # 得到更新后的中心点
    return cent, cluster_assessment


vec_array, id_map, vec = loader(2000)
centroids, ca = k_means(w2idx=id_map, data_set=vec_array, k=20)
for i in range(0, len(ca)):
    print(str(ca[i].tolist()[0][0])+":  "+vec[i][0])
print("fuck")

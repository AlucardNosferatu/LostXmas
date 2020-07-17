import numpy as np

m = np.array(
    [
        [1.0, 2.0],
        [1.0, 2.0]
    ]
)
# 行列式
svd = np.linalg.svd(m)
print(svd)

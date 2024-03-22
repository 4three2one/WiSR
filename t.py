import numpy as np
from sklearn.decomposition import FastICA

# 假设有一个观测信号矩阵 X，其中每一行是一个观测信号
X = np.array([[1, 2, 3, 4],
              [2, 4, 6, 8],
              [3, 6, 9, 12]])

# 创建 ICA 对象
ica = FastICA(n_components=3)

# 应用 ICA 进行信号分离
S = ica.fit_transform(X)

# 重构信号
X_reconstructed = ica.inverse_transform(S)
# 计算去噪后的信号
X_denoised = X - X_reconstructed

# 打印结果
print("原始信号：")
print(X)
print("\n分离的源信号：")
print(S)
print("\n重构后的信号：")
print(X_reconstructed)
print("\n去噪后的信号：")
print(X_denoised)
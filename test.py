import numpy as np
from scipy import signal

np.random.seed(0)
n_samples = 2000
time = np.linspace(0, 8, n_samples)

waft1 = np.sin(2 * time)
waft2 = np.sign(3 * time)
waft3 = signal.sawtooth(2 * np.pi * time)
print('正弦信号为: \n', waft1,
      '方波信号为: \n', waft2,
      '锯齿信号为: \n', waft3)

waft = np.c_[waft1, waft2, waft3]
waft += 0.2 * np.random.normal(size=waft.shape)
waft /= waft.std(axis=0)
arr = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])
mix_waft = np.dot(waft, arr.T)
print('混淆信号为: \n', mix_waft)
print(mix_waft.shape)
from sklearn.decomposition import FastICA

ica = FastICA(n_components=3).fit(mix_waft)
print('ICA模型为: \n', ica)

ica_mixing = ica.mixing_
print('ICA使用的混淆矩阵: \n', ica_mixing)
print(ica_mixing.shape)
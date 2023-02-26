import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# neg_calls = pd.read_csv('train_data/calls.csv',header=None,nrows=8000)
# pos_calls = pd.read_csv('train_data/calls.csv',header=None,skiprows=8000,nrows=8000)


# neg_calls_3d = np.reshape(neg_calls.values, (8000, 50, 40))
# sum_100_2d = np.sum(neg_calls_3d, axis=0)
# pos_calls_3d = np.reshape(pos_calls.values, (8000, 50, 40))
# psum_100_2d = np.sum(pos_calls_3d, axis=0)

# fig1 = plt.figure()
# plt.imshow(psum_100_2d, cmap='inferno')

# fig2 = plt.figure()
# plt.imshow(sum_100_2d, cmap='inferno')

# plt.show()

neg_packed = pd.read_csv('train_data2/other.csv',header=None,nrows=26406)
pos_packed = pd.read_csv('train_data2/other.csv',header=None,skiprows=26406,nrows=29301)

neg_tamper_ratio = np.sum(neg_packed[0])/26406
neg_packed_ratio = np.sum(neg_packed[1])/26406

pos_tamp_ratio = np.sum(pos_packed[0])/29301
pos_packed_ratio = np.sum(pos_packed[1])/29301

print("Tampered ratio for negative samples: ",neg_tamper_ratio)
print("Packed ratio for negative samples: ",neg_packed_ratio)
print("Tampered ratio for positive samples: ",pos_tamp_ratio)
print("Packed ratio for positive samples: ",pos_packed_ratio)

# Tampered ratio for negative samples:  0.459125
# Packed ratio for negative samples:  0.0685
# Tampered ratio for positive samples:  0.68125
# Packed ratio for positive samples:  0.42
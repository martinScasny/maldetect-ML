import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math



def branchCheck():
    neg_calls = pd.read_csv('train_data3/callsPos.csv',header=None,nrows=25000)
    pos_calls = pd.read_csv('train_data3/callsPos.csv',header=None,skiprows=26406,nrows=25000)
    # neg_calls_3d = np.reshape(neg_calls.values, (25000, 36, 36))
    # sum_100_2d = np.sum(neg_calls_3d, axis=0)
    size = math.ceil(math.sqrt(len(neg_calls.values[0])))
    pad = size ** 2 - neg_calls.values.shape[1]
    pad_width = ((0, 0), (0, pad))
    print("pad je",pad)
    neg_calls = np.pad(neg_calls.values, pad_width, mode='constant', constant_values=0)
    pos_calls = np.pad(pos_calls.values, pad_width, mode='constant', constant_values=0)
    print(neg_calls.shape)

    size = int(math.sqrt(len(neg_calls[0])))
    print(size)
    neg_calls_3d = np.reshape(neg_calls, (25000, size, size))
    sum_100_2d = np.sum(neg_calls_3d, axis=0)

    pos_calls_3d = np.reshape(pos_calls, (25000, size, size))
    psum_100_2d = np.sum(pos_calls_3d, axis=0)


    # pos_calls_3d = np.reshape(pos_calls.values, (25000, 36, 36))
    # psum_100_2d = np.sum(pos_calls_3d, axis=0)

    fig1 = plt.figure()
    plt.imshow(psum_100_2d, cmap='inferno', vmin=0, vmax=1000)

    fig2 = plt.figure()
    plt.imshow(sum_100_2d, cmap='inferno', vmin=0, vmax=1000)

    plt.show()

def packedCheck():
    neg_packed = pd.read_csv('train_data3/other.csv',header=None,nrows=26406)
    pos_packed = pd.read_csv('train_data3/other.csv',header=None,skiprows=26406,nrows=29301)

    neg_tamper_ratio = np.sum(neg_packed[0])/26406
    neg_packed_ratio = np.sum(neg_packed[1])/26406

    pos_tamp_ratio = np.sum(pos_packed[0])/29301
    pos_packed_ratio = np.sum(pos_packed[1])/29301

    print("Tampered ratio for negative samples: ",neg_tamper_ratio)
    print("Packed ratio for negative samples: ",neg_packed_ratio)
    print("Tampered ratio for positive samples: ",pos_tamp_ratio)
    print("Packed ratio for positive samples: ",pos_packed_ratio)
    

packedCheck()
# Tampered ratio for negative samples:  0.459125
# Packed ratio for negative samples:  0.0685
# Tampered ratio for positive samples:  0.68125
# Packed ratio for positive samples:  0.42
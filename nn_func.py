import tensorflow as tf
from collectFeatures import collectFeaturesFromFile
import pandas as pd
import numpy as np

model = tf.keras.models.load_model("model")
topNgrams = list(map(int,pd.read_csv("topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
topCalls = pd.read_csv("topFeatures/posCalls.csv",delimiter=";").columns.tolist()

def predict(filepath):
    features, hash = collectFeaturesFromFile(filepath, topNgrams, topCalls)
    prediction = model.predict(features[0][0])
    print(prediction)
    return round(float(prediction), 2), hash

# x1 = pd.read_csv('train_data3/ngram.csv',header=None)
# y = pd.read_csv('train_data3/val.csv',header=None)

# model.predict(x1)

# y_pred = model.predict(x1)
# # Convert the predicted probabilities to binary labels
# y_pred = (y_pred > 0.5)

# # Convert the labels to numpy arrays
# y_true = np.array(y)
# y_pred = np.array(y)

# # Calculate the true positive, true negative, false positive, and false negative values
# tp = np.sum((y_true == 1) & (y_pred == 1))
# tn = np.sum((y_true == 0) & (y_pred == 0))
# fp = np.sum((y_true == 0) & (y_pred == 1))
# fn = np.sum((y_true == 1) & (y_pred == 0))
# print(f"True Positives: {tp/(tp+fp)}%")
# print(f"True Negatives: {tn/(tn+fn)}%")
# print(f"False Positives: {fp/(fp+tp)}%")
# print(f"False Negatives: {fn/(tn+fn)}%")
# print(tp,tn,fp,fn)
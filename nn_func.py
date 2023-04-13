import tensorflow as tf
from collectFeatures import collectFeaturesForNI, collectFeaturesForBI
import pandas as pd

model_BI = tf.keras.models.load_model("model_BI")
model_NI = tf.keras.models.load_model("model_NI")
topNgrams = list(map(int,pd.read_csv("topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
topCalls = pd.read_csv("topFeatures/posCalls.csv",delimiter=";").columns.tolist()

def predict(filepath, model=0):

    if not model:
        features, hash = collectFeaturesForNI(filepath, topNgrams)
        prediction = model_NI.predict(features)
    if model:
        features, hash = collectFeaturesForBI(filepath, topCalls)
        prediction = model_BI.predict(features)
    print(prediction)
    return round(float(prediction), 2), hash

import tensorflow as tf
import collectFeatures
import pe_parser
import pandas as pd


model = tf.keras.models.load_model("model_type4_60k")


def predict(input):
    prediction = model.predict(input)
    return int(prediction > 0.5)

topNgrams = list(map(int,pd.read_csv("topFeatures/posGrams.csv",delimiter=";").columns.tolist()))
topCalls = pd.read_csv("topFeatures/posCalls.csv",delimiter=";").columns.tolist()
features = collectFeatures.collectFeaturesFromFile("Anti-malware-tool/sample", topNgrams, topCalls)
# df = pd.DataFrame(features2)
# print(df.shape)

print(predict(features))

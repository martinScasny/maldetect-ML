import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# x1 = pd.read_csv('train_data3/ngram.csv',header=None)
x2 = pd.read_csv('train_data4/callsPos.csv',header=None)

# x3 = pd.read_csv('train_data3/inst.csv',header=None)
x4 = pd.read_csv('train_data4/imports.csv',header=None)
# x5 = pd.read_csv('train_data3/other.csv',header=None)
y = pd.read_csv('train_data4/val.csv',header=None)

# print(x1.shape,x2.shape,x3.shape,x4.shape,x5.shape,y.shape)

x2_train, x2_test,x4_train, x4_test, y_train, y_test = train_test_split(
    x2,x4,y,test_size=0.2,random_state=42, shuffle=True)

# x2_train, x2_test, y_train, y_test = train_test_split(
#     x2,y,test_size=0.2,random_state=42, shuffle=True)

def createModel(learning_rate, in_calls,in_imports):
  inputBranches = tf.keras.layers.Input(shape=(in_calls.shape[1],))
  x = tf.keras.layers.Dropout(0.3)(inputBranches)
  x = tf.keras.layers.Dense(32, activation='relu')(x)
  inputImports = tf.keras.layers.Input(shape=(in_imports.shape[1],))
  x = tf.keras.layers.concatenate([x, inputImports])
  x = tf.keras.layers.Dense(64, activation='relu')(x)
  x = tf.keras.layers.Dense(32, activation='relu')(x)
  output = tf.keras.layers.Dense(1, activation='sigmoid')(x)
  model = tf.keras.Model(inputs=[inputBranches, inputImports], outputs=output)
  model.compile(optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                loss='binary_crossentropy',
                metrics=['accuracy'])

  return model

def train_model(model, x_train, y_train, x_test, y_test, epochs,
                batch_size=None):
  """Train the model by feeding it data."""

  # history = model.fit(x=features, y=labels, batch_size=batch_size,
  #                     epochs=epochs, shuffle=True) 
  history = model.fit(x_train, y_train, epochs = epochs, validation_split=0.15, validation_data=(x_test,y_test), batch_size=batch_size, verbose=True)
  # model.save("model_BI")

  # The list of epochs is stored separately from the rest of history.
  # epochs = history.epoch
  
  # To track the progression of training, gather a snapshot
  # of the model's mean squared error at each epoch. 

  # hist = pd.DataFrame(history.history)
  # acc = hist["accuracy"]

  return history

# The following variables are the hyperparameters.
learning_rate = 0.001
epochs = 50
batch_size = 128

x_train = [x2_train, x4_train]
x_test = [x2_test, x4_test]
# Establish the model's topography.
# model = createModel(learning_rate, x1,x2,x3,x4,x5)
model = createModel(learning_rate, x2, x4)

# Train the model on the normalized training set. We're passing the entire
# normalized training set, but the model will only use the features
# defined by the feature_layer.
history = train_model(model, x_train, y_train, x_test, y_test,
                      epochs, batch_size)

# After building a model against the training set, test that model
# against the test set.

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss vs. epochs')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc='upper right')
plt.show() 
model.summary()

y_pred = model.predict(x_test)
# Convert the predicted probabilities to binary labels
y_pred = (y_pred > 0.5)

# Convert the labels to numpy arrays
y_true = np.array(y_test)
y_pred = np.array(y_pred)

# Calculate the true positive, true negative, false positive, and false negative values
tp = np.sum((y_true == 1) & (y_pred == 1))
tn = np.sum((y_true == 0) & (y_pred == 0))
fp = np.sum((y_true == 0) & (y_pred == 1))
fn = np.sum((y_true == 1) & (y_pred == 0))
print(f"True Positives: {tp/(tp+fp)}%")
print(f"True Negatives: {tn/(tn+fn)}%")
print(f"False Positives: {fp/(fp+tp)}%")
print(f"False Negatives: {fn/(tn+fn)}%")
print(tp,tn,fp,fn)
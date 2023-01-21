import tensorflow as tf
from collectFeatures import *
    

if __name__ == '__main__':
    # TODO save to file for later use
    # pathToPositiveSamples = r'C:\Users\Martin\Desktop\pos_samples\Win32_EXE2021\test'
    # pathToNegativeSamples = r'C:\Users\Martin\Desktop\negativeSamples'
    # # posNgrams = collectTopNGrams(pathToPositiveSamples,4,10000) - collectTopNGrams(pathToNegativeSamples,4,10000)
    # posCalls = collectTopCallsDump(pathToPositiveSamples,2000)
    # negCalls = collectTopCallsDump(pathToNegativeSamples,2000)
    # print(len(posCalls),len(negCalls))
    # calls = posCalls - negCalls
    # print(len(calls))
    # posNgramsFile = open(r'posCalls.csv','w')
    # result = ""
    
    # for item in calls:
    #     result += str(item)
    #     result += ";"
    # result = result[:-1]
    # posNgramsFile.write(result)
    # posNgramsFile.close()
    
    
    
    
    
    # posCalls = collectTopCallsDump(pathToPositiveSamples,1000) - collectTopCallsDump(pathToNegativeSamples,1000)
    # posCallsFile = open('posCalls.txt','w')
    # posCallsFile.write(posCalls)
    
    
    # Load the data to x,y from files posNgrams.txt and posCalls.txt with keras API
    x,y = tf.keras.datasets.imdb

    # Build the model
    inputNgram = tf.keras.layers.Input(shape=(1337,))
    inputNgram = tf.keras.layers.Dense(64, activation='relu')(inputNgram)
    inputNgram = tf.keras.layers.Dense(1, activation='softmax')(inputNgram)
    inputCalls = tf.keras.layers.Input(shape=(1514,))
    inputCalls = tf.keras.layers.Dense(64, activation='relu')(inputCalls)
    inputCalls = tf.keras.layers.Dense(1, activation='softmax')(inputCalls)
    inputInsRatio = tf.keras.layers.Input(shape=(9,))
    inputInsRatio = tf.keras.layers.Dense(32, activation='relu')(inputInsRatio)
    inputInsRatio = tf.keras.layers.Dense(1, activation='softmax')(inputInsRatio)
    model = tf.keras.layers.Input(shape=((52+1+1),))
    model = tf.keras.layers.concatenate([inputNgram,inputCalls,inputInsRatio,model])
    model = tf.keras.layers.Dense(64, activation='relu')(model)
    model = tf.keras.layers.Dense(2, activation='softmax')(model)
    
    
    

    # Compile the model
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Train the model
    model.fit(X, y, epochs=10)

    # Save the model
    model.save('nn_model.h5')

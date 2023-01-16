# import tensorflow as tf
from collectFeatures import *
    

if __name__ == '__main__':
    # TODO save to file for later use
    pathToPositiveSamples = r'C:\Users\Martin\Desktop\pos_samples\Win32_EXE2021\test'
    pathToNegativeSamples = r'C:\Users\Martin\Desktop\negativeSamples'
    posNgrams = collectTopNGrams(pathToPositiveSamples,4,10000) - collectTopNGrams(pathToNegativeSamples,4,10000)
    posNgramsFile = open(r'posNgrams.csv','w')
    result = ""
    for item in posNgrams:
        result += str(item)
        result += ";"
    result = result[:-1]
    posNgramsFile.write(result)
    posNgramsFile.close()
    
    
    
    
    
    # posCalls = collectTopCallsDump(pathToPositiveSamples,1000) - collectTopCallsDump(pathToNegativeSamples,1000)
    # posCallsFile = open('posCalls.txt','w')
    # posCallsFile.write(posCalls)
    
    
    # # Load the data to x,y from files posNgrams.txt and posCalls.txt with keras API
    # x,y = tf.keras.datasets.imdb

    # # Build the model
    # model = tf.keras.models.Sequential([
    #     tf.keras.layers.Dense(16, activation='relu', input_shape=(X.shape[1],)),
    #     tf.keras.layers.Dense(16, activation='relu'),
    #     tf.keras.layers.Dense(1, activation='sigmoid')
    # ])

    # # Compile the model
    # model.compile(optimizer='adam',
    #               loss='binary_crossentropy',
    #               metrics=['accuracy'])

    # # Train the model
    # model.fit(X, y, epochs=10)

    # # Save the model
    # model.save('nn_model.h5')

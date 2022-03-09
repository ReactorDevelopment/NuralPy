import os.path
import time
import numpy as np
from NeuralNet import NeuralNet
import tensorflow as tf


def flatten(dataPoints):
    return [i for sub in dataPoints for i in sub]


def toTuple(a):
    try:
        return tuple(toTuple(i) for i in a)
    except TypeError:
        return a


if __name__ == "__main__":
    dateset = tf.keras.datasets.mnist
    (imgTrain, classTrain), (imgTest, classTest) = dateset.load_data()

    imgTrain = tf.keras.utils.normalize(imgTrain, axis=1)
    imgTest = tf.keras.utils.normalize(imgTest, axis=1)
    saveResume = False
    trainSet = ([], [])
    testSet = ([], [])
    testLim = 100
    trainLim = testLim * .8
    score = 0
    tests = 0
    i = 0
    net = NeuralNet([784, 128, 128, 10])
    """if saveResume and os.path.exists("weights.csv"):
        net.loadWeights("weights.csv")"""
    while tests < testLim:
        """if classTrain[i] != 1 and classTrain[i] != 6:
            i += 1
            continue"""
        rawTrain = flatten(toTuple(imgTrain[i]))
        rawClass = [0] * 10
        for j in range(0, 10):
            if j == classTrain[i]:
                rawClass[j] = 1
        if tests < trainLim:
            trainSet[0].append(rawTrain)
            trainSet[1].append(rawClass)
        else:
            testSet[0].append(rawTrain)
            testSet[1].append(rawClass)
        i += 1
        tests += 1
        # print("Final Output: " + str(out["output"]) + ", Desired output: " + str(rawClass) + ", Error: " + str(out["error"] * 100) + "%")
    tests = 0
    """while len(trainSet[0]) > 0:
        t = time.time()
        out = net.train(np.array([trainSet[0]]), np.array([trainSet[1]]), epochs=200, learningRate=0.5)
        print("Training ("+str(tests+1)+"/"+str(trainLim)+"), "+str(time.time()-t)+"s, Correct: "+str(trainSet[1][0].index(max(trainSet[1][0]))))
        trainSet[0].pop(0)
        trainSet[1].pop(0)
        tests += 1"""

    t = time.time()
    out = net.train(np.array(trainSet[0]), np.array(trainSet[1]), epochs=1000, learningRate=0.5)
    print("Trained after " + str(time.time() - t) + "s")
    print("================================\n\n==============================")
    t = time.time()
    sampleSet = np.c_[np.array(testSet[0]), np.ones((np.array(testSet[0]).shape[0]))]
    loss = net.loss(np.array(sampleSet), np.array(testSet[1]))
    print("Loss: " + str(loss[0]) + ", Correct: " + str(loss[1] * 100) + "%")

    """
    guess = net.test(rawTrain)
    print("Guess for sample "+str(i)+": "+str(guess.index(max(guess)))+", Correct answer: "+str(rawClass.index(max(rawClass))))
    score += 1 if guess.index(max(guess)) == rawClass.index(max(rawClass)) else 0
    print("Percentage Correct: "+str(score/(tests-trainLim+1)*100)+"%")
    """
    """if saveResume:
        net.saveWeights("weights.csv")"""

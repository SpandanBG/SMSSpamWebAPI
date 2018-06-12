#!/usr/bin/python

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import modules as m

def readData():
    data = pd.read_csv("spam.csv", encoding="latin-1")
    data = data.drop(["Unnamed: 2","Unnamed: 3","Unnamed: 4"], axis=1)
    data = data.rename(columns = {"v1":"label", "v2":"message"})
    data["length"] = data["message"].apply(len)
    return data

def getVectorizerAndFeature(data):
    text_feat = data["message"].copy()
    text_feat = text_feat.apply(m.text_process)
    text_feat = text_feat.apply(m.stemmer)
    vectorizer = TfidfVectorizer("english")
    features = vectorizer.fit_transform(text_feat)
    lf = data["length"].values
    newfeat = np.hstack((features.todense(), lf[:, None]))
    return vectorizer, newfeat

def createModel(features, label):
    mnb = MultinomialNB(alpha=0.2)
    mnb.fit(features, label)
    return mnb

if __name__ == "__main__":
    print("Reading dataset")
    dataSet = readData()
    print("Extracting features")
    vectorizer, features = getVectorizerAndFeature(dataSet)
    print("Creating model")
    model = createModel(features, dataSet["label"])
    print("Saving utils")
    m.saveUtils(model, vectorizer)
    print("Done")
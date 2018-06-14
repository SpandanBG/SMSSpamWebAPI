#!/usr/bin/python

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from bin import modules as m
from db import modules as dbm
import rethinkdb as r

def readData():
    data = pd.read_csv("spam.csv", encoding="latin-1")
    data = data.drop(["Unnamed: 2","Unnamed: 3","Unnamed: 4"], axis=1)
    data = data.rename(columns = {"v1":"label", "v2":"message"})
    data["length"] = data["message"].apply(len)
    return data

def extractLabelWithVote(predicted, spam, ham):
    total = spam + ham
    label = None
    if spam > ham and 'spam' != predicted:
        percent = (spam*100)/total
        if percent >= 80:
            label = 'spam'
    elif spam > ham and 'spam' == predicted:
        label = 'spam'
    elif ham > spam and 'ham' != predicted:
        percent = (ham*100)/total
        if percent >= 80:
            label = 'ham'
    elif ham > spam and 'ham' == predicted:
        label = 'ham'
    else:
        label = predicted
    return label

def getDBDataSet():
    dataSet = {"label": [], "message": []}
    for doc in dbm.msgListGet():
        if doc['ham'] + doc['spam'] >= 50:
            lable = extractLabelWithVote(doc['predicted'], doc['spam'], doc['ham'])
            dataSet['label'].append(lable) 
            dataSet['message'].append(doc['message'])
    dataSet = pd.DataFrame(dataSet)
    dataSet['length'] = dataSet['message'].apply(len)
    return dataSet

def getVectorizerAndFeature(data):
    text_feat = data["message"].copy()
    text_feat = text_feat.apply(m.text_process)
    text_feat = text_feat.apply(m.stemmer)
    vectorizer = TfidfVectorizer("english")
    features = vectorizer.fit_transform(text_feat)
    len_feat = data["length"].values
    features = np.hstack((features.todense(), len_feat[:, None]))
    return vectorizer, features

def createModel(features, label):
    mnb = MultinomialNB(alpha=0.2)
    mnb.fit(features, label)
    return mnb

if __name__ == "__main__":
    print("Loading dataset")
    config = m.loadConfig()
    dbm.dbConnect(config['db'])
    dataSet = readData().append(getDBDataSet(), ignore_index=True)
    print("Extracting features")
    vectorizer, features = getVectorizerAndFeature(dataSet)
    print("Creating model")
    model = createModel(features, dataSet["label"])
    print("Saving utils")
    m.saveUtils(model, vectorizer)
    print("Done")
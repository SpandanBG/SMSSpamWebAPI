import numpy as np
import pandas as pd
import pickle, string
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

def saveUtils(model, vectorizer):
    pickle.dump(model, open("model.sav", "wb"))
    pickle.dump(vectorizer, open("vectorizer.sav", "wb"))

def loadUtils():
    model = pickle.load(open("bin\\model.sav", "rb"))
    vectorizer = pickle.load(open("bin\\vectorizer.sav", "rb"))
    return model, vectorizer

def text_process(text):
    text = text.translate(str.maketrans('','',string.punctuation))
    text = [word for word in text.split() if word.lower() not in stopwords.words("english")]
    return " ".join(text)

def stemmer(text):
    words = ""
    for i in text.split():
        stemmer = SnowballStemmer("english")
        words += (stemmer.stem(i)) + " "
    return words

def extractFeatures(json, vectorizer):
    msg = pd.DataFrame(json)
    msg["length"] = msg["message"].apply(len)
    msgFeat = msg["message"].copy()
    msgFeat = msgFeat.apply(text_process)
    msgFeat = msgFeat.apply(stemmer)
    feats = vectorizer.transform(msgFeat)
    msgLen = msg["length"].values
    return np.hstack((feats.todense(), msgLen[:, None]))

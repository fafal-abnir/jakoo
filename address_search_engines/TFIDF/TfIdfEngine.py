import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim


class TfIdf:
    def __init__(self,file_path):
        self.addresses_name=[]
        self.addresses_importance=[]
        with open(file_path) as f:
            addresses = f.readlines()
        for address in addresses:
            address_name = re.sub("\d+\.\d+","",address)
            address_importance = re.findall("\d+\.\d+",address)[0]
            self.addresses_name.append(address_name)
            self.addresses_importance.append(address_importance)
        self.tfidf = TfidfVectorizer()  # Fit the TfIdf model
        self.tfidf.fit(self.addresses_name)  # Transform the TfIdf model
        self.tfidf_tran = self.tfidf.transform(self.addresses_name)
        self.vocabulary = list(self.tfidf.vocabulary_.keys())

    def gen_vector_T(self, tokens):
        Q = np.zeros((len(self.vocabulary)))

        # print(tokens[0].split(','))
        for token in tokens.split():
            x = self.tfidf.transform([tokens])
            print(token)
            try:
                ind = self.vocabulary.index(token)
                Q[ind] = x[0, self.tfidf.vocabulary_[token]]
            except:
                pass
        return Q

    def top_k_with_cosine_similarity(self, k, query):
        d_cosines = []

        query_vector = self.tfidf.transform([query])
        for d in self.tfidf_tran:
            d_cosines.append(cosine_sim(query_vector.A.flatten(), d.A.flatten()))

        out = np.array(d_cosines).argsort()[-k:][::-1]
        # print("")
        d_cosines.sort()
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'Subject'] = self.addresses_name[index]
        for j, simScore in enumerate(d_cosines[-k:][::-1]):
            a.loc[j, 'Score'] = simScore
        return a







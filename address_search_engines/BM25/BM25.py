import time

import numpy as np
import pandas as pd
import re
from rank_bm25 import BM25Okapi

class BM25Engine:
    def __init__(self,file_path):
        tokenized_addresses = []
        self.addresses_name=[]
        self.addresses_importance=[]
        with open(file_path) as f:
            addresses = f.readlines()
        for address in addresses:
            address_name = re.sub("\d+\.\d+","",address)
            address_importance = re.findall("\d+\.\d+",address)[0]
            self.addresses_name.append(address_name)
            tokenized_addresses.append(address_name.split(" "))
            self.addresses_importance.append(address_importance)
        self.bm25 = BM25Okapi(tokenized_addresses)

    def top_k_with_cosine_similarity(self, k, query):
        tokenized_query = query.split(" ")
        # self.bm25.get_top_n(tokenized_query, self.addresses_name, n=k)
        scores = self.bm25.get_scores(tokenized_query)
        # print("")
        out = np.array(scores).argsort()[-k:][::-1]

        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'Subject'] = self.addresses_name[index]
        # for j, simScore in enumerate(d_cosines[-k:][::-1]):
            a.loc[i, 'Score'] = scores[index]
        return a


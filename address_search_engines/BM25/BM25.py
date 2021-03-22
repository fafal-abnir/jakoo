import csv
from operator import methodcaller

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi


class BM25Engine:
    def __init__(self, file_path):
        print("start loading BM25Engine")
        self.addresses_name = []
        self.addresses_importance = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.addresses_name.append(row.get('text'))
                self.addresses_importance.append(row.get('importance'))
        tokenized_addresses = list(map(methodcaller("split", " "), self.addresses_name))
        self.bm25 = BM25Okapi(tokenized_addresses)
        print("finished loading BM25Engine")

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

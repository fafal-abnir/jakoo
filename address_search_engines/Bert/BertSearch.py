import time

import h5py
import numpy as np
import pandas as pd
from enum import Enum
from sentence_transformers import SentenceTransformer, util
from sklearn.neighbors import KDTree, BallTree


class IndexType(Enum):
    BallTree = "BallTree"
    KDTree = "KDTree"
    # RTree = "RTree"


class BertSearch:
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    address_keys = []

    def __init__(self, address_file_name, index_type=IndexType.BallTree):
        if not isinstance(index_type, IndexType):
            raise TypeError('index type must be an instance of IndexType Enum')
        print(index_type.value)
        self.address_values = []
        self.l2Norm_address_values = []
        print("Start loading address")
        start_time = time.time()
        with h5py.File('{}.hdf5'.format(address_file_name), 'r') as f:
            address_count = 0
            x = f.keys()
            for a in x:
                try:
                    self.address_values.append(f[a].value)
                    self.l2Norm_address_values.append(np.array(f[a].value / np.linalg.norm(f[a].value)))
                    self.address_keys.append(a)
                    if (address_count % 1000) == 0:
                        print("Load {} address".format(address_count))
                    address_count = address_count + 1
                except:
                    print(a)
            print("Load address in {} s".format(time.time() - start_time))
            print("Start creating index with Type: {}".format(index_type.value))
            start_time = time.time()
            if index_type == IndexType.KDTree:
                self.index_tree = KDTree(np.array(self.l2Norm_address_values), leaf_size=400)
            elif index_type == IndexType.BallTree:
                self.index_tree = BallTree(np.array(self.l2Norm_address_values), leaf_size=400)
            print("Load address in {} s".format(time.time() - start_time))

    def extract(self, query):
        return self.model.encode(query)

    def cosine_similarity_T(self, k, query):
        d_cosines = []
        query_vector = self.model.encode(query)
        for d in self.address_values:
            d_cosines.append(util.pytorch_cos_sim(query_vector, d).item())
        out = np.array(d_cosines).argsort()[-k:][::-1]
        d_cosines.sort()
        a = pd.DataFrame()
        for i, index in enumerate(out):
            a.loc[i, 'index'] = str(index)
            a.loc[i, 'Subject'] = self.address_keys[index]
        for j, simScore in enumerate(d_cosines[-k:][::-1]):
            a.loc[j, 'Score'] = simScore
        return a

    def top_k_with_cosine_similarity(self, k, query):
        query_vector = self.model.encode(query)
        query_vector = (query_vector / np.linalg.norm(query_vector))
        distances, indexes = self.index_tree.query([query_vector], k)
        a = pd.DataFrame()
        for i in range(len(distances[0])):
            a.loc[i, 'index'] = str(i)
            a.loc[i, 'Subject'] = self.address_keys[indexes[0][i]]
            a.loc[i, 'Score'] = distances[0][i]
        return a

    def test_run(self):
        print(self.extract('تهران آزادی'))



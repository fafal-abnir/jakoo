import time

import h5py
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.neighbors import KDTree


class BertSearch:
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    KD_tree_index = None
    address_keys = []
    address_values = []
    l2Norm_address_values = []

    def __init__(self, address_file_name):
        print("Start loading address")
        start_time = time.time()
        f = h5py.File('../../resources/hdf5/{}.hdf5'.format(address_file_name), 'r')
        address_count = 0
        x = f.keys()
        for a in x:
            self.address_values.append(f[a].value)
            self.l2Norm_address_values.append(np.array(f[a].value / np.linalg.norm(f[a].value)))
            self.address_keys.append(a)
            if (address_count % 1000) == 0:
                print("Load {} address".format(address_count))
            address_count = address_count + 1
        f.close()
        print("Load address in {} s".format(time.time() - start_time))
        print("Start creating index")
        start_time = time.time()
        self.KD_tree_index = KDTree(np.array(self.l2Norm_address_values), leaf_size=400)
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

    def euclidean_similarity_L2norm(self, k, query):
        query_vector = self.model.encode(query)
        query_vector = (query_vector / np.linalg.norm(query_vector))
        distances, indexes = self.KD_tree_index.query([query_vector], k)
        a = pd.DataFrame()
        for i in range(len(distances[0])):
            a.loc[i, 'index'] = str(i)
            a.loc[i, 'Subject'] = self.address_keys[indexes[0][i]]
            a.loc[i, 'Score'] = distances[0][i]
        return a

    def test_run(self):
        print(self.extract('تهران آزادی'))


def main():
    search_engine = BertSearch("tehran-preprocessed")
    while True:
        address = str(input('Please enter address: (enter 0 to end): '))
        if address == '0':
            break
        start_time=time.time()
        print(search_engine.cosine_similarity_T(10, address))
        print("Brute force {}".format(time.time()-start_time))
        start_time = time.time()
        print(search_engine.euclidean_similarity_L2norm(10, address))
        print("Kdtree force {}".format(time.time() - start_time))



if __name__ == '__main__':
    main()

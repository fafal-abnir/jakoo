# import address_search_engines.TFIDF.TfIdfEngine
from address_search_engines.TFIDF.TfIdfEngine import TfIdf
from address_search_engines.BM25.BM25 import BM25Engine

file_path = "./resources/tehran-address"
if __name__ == '__main__':
    # tf = TfIdf(file_path)
    bm = BM25Engine(file_path)
    while True:

        address = str(input('Please enter a String to see the correction: (enter 0 to end): '))
        if address == '0':
            break
        # print("tf")
        # print(tf.top_k_with_cosine_similarity(20,address))
        print("bm")
        print(bm.top_k_with_cosine_similarity(20, address))
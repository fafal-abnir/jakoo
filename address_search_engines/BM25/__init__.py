# from rank_bm25 import BM25Okapi
# import time
# with open("/home/vahid/projects/jakoo/data/tehran-preprocessed") as f:
#     addresses = f.readlines()
#
# tokenized_corpus = [add.split(" ") for add in addresses]
#
# bm25 = BM25Okapi(tokenized_corpus)
#
# star_time = time.time()
# query = "تهران شهرقدس گالری پرده ترمه"
# tokenized_query = query.split(" ")
#
# doc_scores = bm25.get_scores(tokenized_query)
# print(bm25.get_top_n(tokenized_query, tokenized_corpus, n=10))
# print(time.time()-star_time)
# # array([0.        , 0.93729472, 0.        ])
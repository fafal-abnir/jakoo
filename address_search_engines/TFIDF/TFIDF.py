# import numpy as np
# import pandas as pd
# with open('../../resources/2k-tehran-preprocessed') as f:
#     addresses = f.readlines()
#
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# tfidf = TfidfVectorizer()  # Fit the TfIdf model
# tfidf.fit(addresses)  # Transform the TfIdf model
# tfidf_tran = tfidf.transform(addresses)
# vocabulary = list(tfidf.vocabulary_.keys())
#
#
# def gen_vector_T(tokens):
#     Q = np.zeros((len(vocabulary)))
#
#     # print(tokens[0].split(','))
#     for token in tokens.split():
#         x = tfidf.transform([tokens])
#         print(token)
#         try:
#             ind = vocabulary.index(token)
#             Q[ind] = x[0, tfidf.vocabulary_[token]]
#         except:
#             pass
#     return Q
#
#
# def cosine_similarity_T(k, query):
#     d_cosines = []
#
#     query_vector = tfidf.transform([query])
#     for d in tfidf_tran:
#         d_cosines.append(cosine_sim(query_vector.A.flatten(), d.A.flatten()))
#
#     out = np.array(d_cosines).argsort()[-k:][::-1]
#     # print("")
#     d_cosines.sort()
#     a = pd.DataFrame()
#     for i, index in enumerate(out):
#         a.loc[i, 'index'] = str(index)
#         a.loc[i, 'Subject'] = addresses[index]
#     for j, simScore in enumerate(d_cosines[-k:][::-1]):
#         a.loc[j, 'Score'] = simScore
#     return a
#
#
#
# def cosine_sim(a, b):
#     cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
#     return cos_sim
#
#
# while True:
#     address = str(input('Please enter a String to see the correction: (enter 0 to end): '))
#     if address == '0':
#         break
#     print(cosine_similarity_T(20,address))
#

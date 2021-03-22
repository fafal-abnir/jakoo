import time

import pandas as pd

from address_preprocessing.TextPreprocessing import preprocess_address
from address_search_engines.BM25.BM25 import BM25Engine
from address_search_engines.Bert.BertSearch import BertSearch

if __name__ == '__main__':
    address_file_path = 'resources/tehran.csv'
    test_file_path = 'resources/Addresses-test-2.xlsx'
    # tf = TfIdf(file_path)
    # bm = BM25Engine(address_file_path)
    bert = BertSearch('resources/tehran-address')
    df = pd.read_excel(test_file_path)
    total = 0
    correct = 0
    k = 5
    rows = []
    evaluate_df = pd.DataFrame()
    for index, row in df.iterrows():
        isFind = False
        if total % 100 == 0:
            print(correct)
        if type(row['query']) is str and type(row['address']) is str:
            start_time = time.time()
            query = row['query']
            target_address = row['address']
            if preprocess_address(target_address) in bert.top_k_with_cosine_similarity(k, query)['Subject'].tolist():
                isFind = True
                correct += 1
            total += 1
            execution_time = time.time() - start_time
            query_length = len(query)
            rows.append([query, query_length, isFind, execution_time])
            # evaluate_df.append(new_row, ignore_index=True)
    print(correct/total)
    evaluate_df = pd.DataFrame(rows,columns=['query', 'length', 'isFind', 'execution_time'])
    evaluate_df.to_excel("output.xlsx")

import pandas as pd
import time
import tensorflow_hub as hub
from sklearn.metrics.pairwise import linear_kernel
from address_search_engines.USE.TrainUSE import embed

start_time = time.time()
with open('../../resources/preprocessed.txt') as f:
    lines = f.readlines()
print("time to load file time => {}".format(time.time() - start_time))
# addresses = list(map(preprocess_address, lines))
print(lines[0:10])
start_time = time.time()
model = hub.load("../4")  # Create function for using model training
address_vec = model(lines[0:20000])
print("time to encode addresses=> {}".format(time.time() - start_time))
def SearchDocument(query):
    q = [query]
    # embed the query for calcluating the similarity
    Q_Train = embed(q)


    # loadedmodel =imported_m.v.numpy()
    # Calculate the Similarity
    linear_similarities = linear_kernel(Q_Train, address_vec).flatten()
    # Sort top 10 index with similarity score
    Top_index_doc = linear_similarities.argsort()[:-11:-1]
    # sort by similarity score
    linear_similarities.sort()
    a = pd.DataFrame()
    for i, index in enumerate(Top_index_doc):
        a.loc[i, 'index'] = str(index)
        a.loc[i, 'File_Name'] = lines[index]  ## Read File name with index from File_data DF
    for j, simScore in enumerate(linear_similarities[:-11:-1]):
        a.loc[j, 'Score'] = simScore
    return a

print("-----------------------------")
while True:
    address = str(input('Please enter a String to see the correction: (enter 0 to end): '))
    if address == '0':
        break
    print(SearchDocument(address))
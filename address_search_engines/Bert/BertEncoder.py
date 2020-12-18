import time

import h5py
from sentence_transformers import SentenceTransformer

address_file_name = "tehran-preprocessed"
with open('../../resources/{}'.format(address_file_name)) as f:
    addresses = f.readlines()

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

start_time = time.time()
f = h5py.File('../../resources/hdf5/{}.hdf5'.format(address_file_name), 'a')
address_count = 0
for address in addresses:
    if not (address in f):
        address_count = address_count + 1
        if address_count % 1000==0:
            print('Encode {} address'.format(address_count))
        f.create_dataset(address, data=model.encode(address))
print('Encode {} with bert in {} s '.format(address_count, time.time() - start_time))
f.close()

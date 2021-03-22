import time
import re
import h5py
import csv
from sentence_transformers import SentenceTransformer


class BertEncoder:
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

    def __init__(self, file_path):
        print("Start loading address")
        start_time = time.time()
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        with h5py.File('{}.hdf5'.format(file_path), 'a') as hdf:
            address_count = 0
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    address_name = row.get('text')
                    if not (address_name in hdf):
                        address_count += 1
                        address_count = address_count + 1
                        if address_count % 1000 == 0:
                            print('Encode {} address'.format(address_count))
                        # print(address_value)
                        if address_name in hdf:
                            continue
                        address_importance =row.get('importance')
                        dataset = hdf.create_dataset(address_name, data=model.encode(address_name))
                        dataset.attrs["importance"] = address_importance
            print('Encode {} with bert in {} s '.format(address_count, time.time() - start_time))

if __name__ == '__main__':
    BertEncoder("../../resources/3k-tehran-address")
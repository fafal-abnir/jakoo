import time
import re
import h5py
from sentence_transformers import SentenceTransformer


class BertEncoder:
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    def __init__(self, file_path):
        print("Start loading address")
        start_time = time.time()
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        hdf = h5py.File('{}.hdf5'.format(file_path), 'a')
        address_count = 0
        # self.addresses_name = []
        # self.addresses_importance = []
        # self.l2Norm_address_values = []
        with open(file_path) as f:
            addresses = f.readlines()
        for address in addresses:
            address_name = re.sub("\d+\.\d+", "", address)
            address_importance = re.findall("\d+\.\d+", address)[0]
            if not (address_name in hdf):
                address_count = address_count + 1
                if address_count % 1000 == 0:
                    print('Encode {} address'.format(address_count))
                # print(address_value)
                if address_name in hdf:
                    continue
                address_importance = re.findall("\d+\.\d+", address)[0]
                dataset = hdf.create_dataset(address_name, data=model.encode(address))
                dataset.attrs["importance"] = address_importance
        print('Encode {} with bert in {} s '.format(address_count, time.time() - start_time))
        hdf.close()

        # f = h5py.File('../../resources/hdf5/{}.hdf5'.format(address_file_name), 'r')

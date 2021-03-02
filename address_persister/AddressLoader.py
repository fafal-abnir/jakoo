import time
import re
import h5py
from sentence_transformers import SentenceTransformer
#
# address_file_name = "3k-tehran-address"
#
#
# with open('../resources/{}'.format(address_file_name)) as f:
#     addresses = f.readlines()
#
#
# start_time = time.time()
# f = h5py.File('../resources/hdf5/{}.hdf5'.format(address_file_name), 'a')
# address_count = 0
# for address in addresses:
#     if not (address in f):
#         address_count = address_count + 1
#         if address_count % 1000 == 0:
#             print('{} address persisted'.format(address_count))
#         address_value = re.sub("\d+\.\d+","",address)
#         # print(address_value)
#         if address_value in f:
#             continue
#         address_importance = re.findall("\d+\.\d+",address)[0]
#         dataset = f.create_dataset(address_value, address)
#         dataset.attrs["importance"] = address_importance
# print('{} of file:{} persisted in hdf5 in {}'.format(address_count, address_file_name, time.time() - start_time))
# f.close()

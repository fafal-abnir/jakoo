from address_preprocessing.TextPreprocessing import preprocess_address
import csv
import re
with open('../resources/tehran-address') as f:
    lines = f.readlines()
c = 0
with open('../resources/tehran.csv','w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["text","importance"])
    for line in lines:
        address_name = re.sub("\d+\.\d+", "", line)
        address_importance = re.findall("\d+\.\d+", line)[0]
        preprocessed_address_name = preprocess_address(address_name)
        if c % 1000 == 0:
            print(c)
        writer.writerow([preprocessed_address_name,address_importance])
        c = c + 1




from address_preprocessing.TextPreprocessing import preprocess_address

with open('../resources/tehran-address') as f:
    lines = f.readlines()
c = 0
with open('../resources/preprocessed.txt', 'a') as the_file:
    for line in lines:
        preprocessed_line = preprocess_address(line) + '\n'
        if c % 1000 == 0:
            print(c)
        the_file.write(preprocessed_line)
        c = c + 1

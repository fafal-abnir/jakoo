from spellchecker import SpellChecker
spell = SpellChecker(language=None)
spell.word_frequency.load_text_file("../resources/tehran-address")
spell.export("../resources/spellcheker")
spell = SpellChecker(language=None, local_dictionary="../resources/spellcheker")

sorted_dict = dict(sorted(spell.word_frequency.dictionary.items(), key=lambda item: item[1],reverse=True))


with open('../resources/words.txt', 'w') as log:
    for key in sorted_dict.keys():
        log.write('{}\n'.format(key))

import gzip
with open('../resources/words.txt', 'rb') as f_in, gzip.open('../resources/words.txt.gz', 'wb') as f_out:
    f_out.writelines(f_in)
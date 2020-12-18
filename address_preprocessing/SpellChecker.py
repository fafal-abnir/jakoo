from spellchecker import SpellChecker
import wordninja

spell = SpellChecker(language=None, local_dictionary="../resources/spellcheker")
while True:
    word = str(input('Please enter a word to see the correction: (enter 0 to end): '))
    if word == '0':
        break
    print('candidates => {}'.format(spell.candidates(word)))
    print('known => {}'.format(spell.known(word)))
    print('correction => {}'.format(spell.correction(word)))
    print('unknown => {}'.format(spell.unknown(word)))
    print('word_probability => {}'.format(spell.word_probability(word)))
    print('=======')
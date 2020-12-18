from math import log
from spellchecker import SpellChecker
import re
import enchant

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
spell = SpellChecker(language=None, local_dictionary="../resources/spellcheker")
words = dict(sorted(spell.word_frequency.dictionary.items(), key=lambda item: item[1], reverse=True))
wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
maxword = max(len(x) for x in words)
enchant_dict=enchant.Dict("fa_IR")


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k

    return " ".join(reversed(out))


def infer_duplicate_space(str):
    # Find the best match for the i first token, assuming cost has
    # been built for the i-1 first token.
    # Returns a pair (match_cost, match_length).
    tokens = str.split()
    if len(tokens) == 1:
        return str
    best_costs = {0: (wordcost.get(tokens[0], 9e999), 0)}

    def best_match(i):
        min_cost = 9e999
        r = i
        for j in range(max(0, i - 5), i + 1):
            joint_words = ''.join(tokens[j:i + 1])
            cost = 9e999
            if j == 0:
                cost = wordcost.get(joint_words, 9e999)
            else:
                cost = wordcost.get(joint_words, 9e999) + best_costs[j - 1][0]
            if cost < min_cost:
                min_cost = cost
                r = j
        return (min_cost, r)

    for t in range(1, len(tokens)):
        best_costs[t] = best_match(t)

    out = []
    i = len(tokens) - 1
    while i >= 0:
        c, k = best_costs[i]
        out.append(''.join(tokens[k:i + 1]))
        i = k - 1
    return " ".join(reversed(out))


def basic_cleaning(str):
    return re.sub(r'[^\w]', '', str)


def spell_correction(str):
    tokens = str.split()
    result = []
    for token in tokens:
        result.append(spell.correction(token))
    return " ".join(result)


def last_token_candidates(str):
    tokens = str.split()
    if len(tokens) == 0:
        return str
    return enchant_dict.suggest(tokens[-1])


def preprocess_address(str):
    clean_str = basic_cleaning(str)
    inferred_spaces = infer_spaces(clean_str)
    spell_corrected = spell_correction(inferred_spaces)
    space_corrected = infer_duplicate_space(spell_corrected)
    final_result = infer_duplicate_space(space_corrected)
    # print(final_result)
    return final_result


while True:
    address = str(input('Please enter a String to see the correction: (enter 0 to end): '))
    if address == '0':
        break
    # print('wordninja => {}'.format(infer_spaces(word)))
    clean_str = basic_cleaning(address)
    print('basic_cleaning => {}'.format(clean_str))
    inferred_spaces = infer_spaces(clean_str)
    print('inferred_spaces => {}'.format(inferred_spaces))
    spell_corrected = spell_correction(inferred_spaces)
    print('spell correction => {}'.format(spell_corrected))
    space_corrected = infer_duplicate_space(inferred_spaces)
    print('duplicate space correction => {}'.format(space_corrected))
    final_result = infer_duplicate_space(space_corrected)
    print('final result => {}'.format(final_result))
    print('last token candidate => {}'.format(last_token_candidates(final_result)))


#!/usr/bin/env python

import re

DICTIONARY = '/usr/share/dict/words'
PLAIN_WORD = re.compile('^[a-zA-Z]+$')
PROCESS_LIMIT = 75000
LETTERS = [
    'R',
    'A',
    'I',
    'S',
    'N',
    'T',
    'O',
    'L',
    'E',
    'C',
    'D',
    'U',
    'G',
    'P',
    'M',
    'H',
    'B',
    'Y',
    'F',
    'V',
    'W',
    'K',
    'Z',
    'X',
    'Q',
    'J',
]

def n_or_more_letters(string, n):
    return len(string) >= n

def contains_letter(string, letter):
    return string.find(letter) >= 0

def nth_letter(string, n, letter):
    try:
        return string[n] == letter
    except:
        return False

def humanify(n):

    suffix = "th"

    if n/10 != 1:
        if n % 10 == 1:
            suffix = "st"
        elif n % 10 == 2:
            suffix = "nd"
        elif n % 10 == 3:
            suffix = "rd"

    return "%d%s" % (n, suffix)

def load_words():

    words = set()

    with open(DICTIONARY) as dictionary:

        for word in dictionary.readlines():
            word = word.rstrip('\n').upper()

            if PLAIN_WORD.match(word):
                words.add(word)

    return words

def main():

    words = load_words()
    questions = 0

    print "Think of a word..."

    while len(words) > 1:

        word_num = float(len(words))
        word_min_len = 1e9
        word_max_len = 0

        for word in words:
            word_len = len(word)
            if word_len < word_min_len: word_min_len = word_len
            if word_len > word_max_len: word_max_len = word_len

        smallest = {
            'distance': 1e9,
            'method': None,
            'arguments': (),
        }

        def test(method, *args):

            count = sum(method(word, *args) for word in words)
            percentage = count/word_num
            distance = abs(percentage - 0.5)

            if distance < smallest['distance']:
                smallest['distance'] = distance
                smallest['method'] = method
                smallest['arguments'] = args

            return percentage

        process_count = 0

        contains_letter
        for letter in LETTERS:
            if process_count > PROCESS_LIMIT: break

            test(contains_letter, letter)
            process_count += len(words)

        # n_or_more_letters
        min_search = word_min_len
        max_search = word_max_len

        while min_search < max_search:
            if process_count > PROCESS_LIMIT: break

            mid_search = (min_search + max_search)/2

            if test(n_or_more_letters, mid_search) > 0.5:
                min_search = mid_search + 1
            else:
                max_search = mid_search

            process_count += len(words)

        # nth_letter
        for n in range(0, word_max_len):
            if process_count > PROCESS_LIMIT: break

            for letter in LETTERS:
                if process_count > PROCESS_LIMIT: break

                test(nth_letter, n, letter)
                process_count += len(words)

        questions += 1
        question = None

        if smallest['method'] == n_or_more_letters:
            question = "Is the word %d or more letters? " % smallest['arguments']

        elif smallest['method'] == contains_letter:
            question = "Does it have the letter %s? " % smallest['arguments']

        elif smallest['method'] == nth_letter:
            question = "Is the %s letter %s? " % ( humanify(smallest['arguments'][0]+1), smallest['arguments'][1] )

        yn = raw_input(question)

        desired_result = yn.lower() == 'y'
        words = filter(lambda word: smallest['method'](word, *smallest['arguments']) == desired_result, words)

    if len(words) == 0:
        print "I don't know what word it is"

    elif len(words) == 1:
        print "The word is: %s" % (words.pop())
        print "That took %d tries" % (questions)

main()

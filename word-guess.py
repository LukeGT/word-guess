#!/usr/bin/env python

import re

DICTIONARY = '/usr/share/dict/words'
PLAIN_WORD = re.compile('^[a-zA-Z]+$')

def n_or_more_letters(string, n):
    return len(string) >= n

def contains_letter(string, letter):
    return string.find(letter) >= 0

def nth_letter(string, n, letter):

    if n >= len(string) or n < -len(string):
        return False

    else:
        return string[n] == letter

def humanify(n):

    suffix = "th"

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

    print "Think of a word..."

    words = load_words()
    questions = 0

    while len(words) > 1:

        word_num = float(len(words))
        word_min_len = min(len(word) for word in words)
        word_max_len = max(len(word) for word in words)

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

        # n_or_more_letters
        for n in range(word_min_len + 1, word_max_len + 1):

            test(n_or_more_letters, n)

        # contains_letter
        for letter_num in range(0, 26):

            letter = chr(letter_num + ord('A'))
            test(contains_letter, letter)

        if word_max_len * 26 * len(words) < 1000000:

            # nth_letter
            for n in range(0, word_max_len):
                for letter_num in range(0, 26):

                    letter = chr(letter_num + ord('A'))
                    test(nth_letter, n, letter)

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
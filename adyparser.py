# -*- coding: utf-8 -*-
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.tokenize import word_tokenize
import nltk

import util
import usaddress


def filter_paren(tup):
    if tup[0] == '(':
        return tup[0], '-NONE-'
    return tup


def probableAddresses(text):
    tokens = word_tokenize(util.preproces_text(text))
    tagged = nltk.pos_tag(tokens)

    # get rid of commas
    tagged = [tup for tup in tagged if tup[0] != ',']

    # flag open paren as -NONE-
    tagged = map(filter_paren, tagged)

    grammer = 'Location: ' \
        '{<CD><NNP>+<JJ>?<NNP>+|' \
        '<CD><NNP><CD><NNP>+|' \
        '<CD>+<NNP>+|' \
        '<CD><NNP>+}'
    chunkParser = nltk.RegexpParser(grammer)
    result = chunkParser.parse(tagged)
    return [s for s in result.subtrees(lambda t: t.label() == 'Location')]


def isValidAddress(ady):
    address = usaddress.parse(ady)
    if len(address) < 5:
        return False

    if any([a[1] == 'Recipient' for a in address]):
        return False
    return True


def parse(text):
    candidates = probableAddresses(text)
    candidates = [util.location_to_string(c) for c in candidates]
    return [c for c in candidates if isValidAddress(c)]

if __name__ == '__main__':
    import codecs

    sample = codecs.open('trainers/ad-trainer1.txt', 'r', encoding='utf8') \
        .read()

    print parse(sample)

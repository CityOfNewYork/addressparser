# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"


import re
import os
import nltk
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
from nltk.tokenize import word_tokenize

import preprocess

def filter_unnecessary_abbreviations(tup):
    rex = re.compile('inc\.$|rest$|corp\.?$', re.IGNORECASE)
    if rex.match(tup[0]):
        return tup[0], '-NONE-'
    return tup


def filter_comma(tup):
    if tup[0] == ',':
        return ',', 'COMMA'
    return tup


def filter_ls(tup):
    # ls (list marker) is not necessarey, should be a digit
    if tup[1] == 'LS':
        return tup[0], 'CD'
    return tup

def filter_throughways(tup):
    '''Identify and tag throughway names.

    '''
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html
    rex = re.compile('(avenue|boulevard|place|plaza|street)', re.IGNORECASE)

    if rex.match(tup[0]):
        # 马路的路
        # MaLu de Lu
        return tup[0], 'LU'
    return tup


def filter_state(tup):
    rex = re.compile('NY$', re.IGNORECASE)
    if rex.match(tup[0]):
        return tup[0], 'STATE'
    return tup


def pos_tag(text, verbose=False):
    tokens = word_tokenize(preprocess.prepare_text(text, verbose))
    tagged = nltk.pos_tag(tokens)

    # retag commas
    tagged = map(filter_comma, tagged)

    # change counting lists (ls) to counting digits (cd)
    tagged = map(filter_ls, tagged)

    # tag street names
    tagged = map(filter_throughways, tagged)

    # tag state
    tagged = map(filter_state, tagged)

    # change POS tag to -NONE- to aid chunking
    # todo: better comments -- remove this function to find
    # cases where this break tests
    return map(filter_unnecessary_abbreviations, tagged)


def chunkAddresses(text, verbose=False):

    tagged = pos_tag(text, verbose)
    if verbose:
        print tagged

    grammer = 'Location: ' \
      '{' \
      '<CD><CD|NNP|JJ|COMMMA>+<LU>?<CD|JJ|NNP|COMMA>+<STATE|COMMA>+' \
      '}'

    chunkParser = nltk.RegexpParser(grammer)
    chunks = chunkParser.parse(tagged)
    locations =  [s for s in chunks.subtrees(lambda t: t.label() == 'Location')]
    if verbose:
        print 'Chunked Locations:'
        if locations:
            for loc in locations:
                print '\t', loc
                print
        else:
            print '\tNone found'
    return locations

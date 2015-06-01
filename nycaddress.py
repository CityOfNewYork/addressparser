# -*- coding: utf-8 -*-
# from nltk.chunk import *
# from nltk.chunk.util import *
# from nltk.chunk.regexp import *
# from nltk import Tree
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import re

import util
import usaddress


def filter_unnecessary_abbreviations(tup):
    rex = re.compile('inc\.$|rest$', re.IGNORECASE)
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


def pos_tag(text, verbose=False):
    tokens = word_tokenize(util.preproces_text(text))
    tagged = nltk.pos_tag(tokens)

    # retag commas
    tagged = map(filter_comma, tagged)

    # change counting lists (ls) to counting digits (cd)
    tagged = map(filter_ls, tagged)

    # change POS tag to -NONE- to aid chunking
    # todo: better comments -- remove this function to find
    # cases where this break tests
    return map(filter_unnecessary_abbreviations, tagged)


def parseAddresses(text, verbose=False):

    tagged = pos_tag(text, verbose)
    if verbose:
        print tagged

    grammer = 'Location: ' \
        '{<CD><NNP|COMMA>+<JJ>?<NNP|COMMA>+|' \
        '<CD><NNP><CD><NNP|COMMA>+|' \
        '<CD>+<NNP|COMMA>+|' \
        '<CD><NNP|COMMA>+}'

    chunkParser = nltk.RegexpParser(grammer)
    result = chunkParser.parse(tagged)
    return [s for s in result.subtrees(lambda t: t.label() == 'Location')]


def showFailureReason(msg, address, components, verbose=False):
    if verbose:
        print 'Failed: %s' % msg
        print '\tAddress:\t\t%s' % address
        print '\tUS Address Components:\t%s\n' % components


def probableAddresses(text, verbose=False):
    locations = []
    # sentences = sent_tokenize(util.preproces_text(text))
    sentences = sent_tokenize(text)
    for s in sentences:
        print 'Sent: %s\n' % s
        if len(s) < 10:
            if verbose:
                showFailureReason('Sentence too short', s, '--', verbose)
            continue
        locs = parseAddresses(s, verbose)
        locations += locs

    return locations


def isValidAddress(ady, verbose=False):

    address = usaddress.parse(ady)
    if len(address) < 4:
        showFailureReason('Not Enough Terms', ady, address, verbose)
        return False

    if any([a[1] == 'Recipient' for a in address]):
        showFailureReason('Recipient', ady, address, verbose)
        return False

    if not any([a[1] == 'StreetName' for a in address]):
        showFailureReason('StreetName', ady, address, verbose)
        return False

    if not any([a[1] == 'AddressNumber' for a in address]):
        showFailureReason('AddressNumber', ady, address, verbose)
        return False

    return True


def parse(text, verbose=False):
    candidates = probableAddresses(text, verbose)
    candidates = [util.location_to_string(c) for c in candidates]

    # only candidates that end in NY
    rex = re.compile('(.+,\s+NY)', re.IGNORECASE)
    candidates = [rex.match(c) for c in candidates]
    candidates = [c.group() for c in candidates if c is not None]

    return [c for c in candidates if isValidAddress(c)]


if __name__ == '__main__':
    import codecs

    sample = codecs.open('tests/ad-sample6.txt', 'r', encoding='utf8') \
        .read()
    for address in parse(sample, False):
        print address

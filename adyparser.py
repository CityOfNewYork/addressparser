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

def filter_unnecessary_abbreviations(tup):
    rex = re.compile( 'inc\.$|rest$', re.IGNORECASE)
    if rex.match(tup[0]):
        return tup[0], '-NONE-'
    return tup

def filter_jj_to_nnp(tup):
    txt = tup[0].lower()
    if txt.endswith('st') or txt.endswith('nd') or \
       txt.endswith('rd') or txt.endswith('th'):
       return tup[0], 'NNP'
    return tup



def probableAddresses(text):
    tokens = word_tokenize(util.preproces_text(text))
    tagged = nltk.pos_tag(tokens)

    # get rid of commas
    tagged = [tup for tup in tagged if tup[0] != ',']

    # flag open paren as -NONE-
    tagged = map(filter_paren, tagged)

    # change POS tag to -NONE- to aid chunking
    # todo: better comments -- remove this function to find
    # cases where this break tests
    tagged = map(filter_unnecessary_abbreviations, tagged)

    # tagged = map(filter_jj_to_nnp, tagged)

    # print tagged

    grammer = 'Location: ' \
        '{<CD><NNP>+<JJ>?<NNP>+|' \
        '<CD><NNP><CD><NNP>+|' \
        '<CD>+<NNP>+|' \
        '<CD><NNP>+}'

    chunkParser = nltk.RegexpParser(grammer)
    result = chunkParser.parse(tagged)
    return [s for s in result.subtrees(lambda t: t.label() == 'Location')]

#  (u'55', 'CD'),
#  (u'Water', 'NNP'),
#  (u'Street', 'NNP'), (u'9th', 'JJ'), (u'Floor', 'NNP'), (u'SW', 'NNP'),
# (u'New', 'NNP'), (u'York', 'NNP'), (u'NY', 'NNP'), (u'10041', 'CD')

def showFailureReason(msg, ady, address, verbose=False):
        if verbose:
            print 'Failed: %s' % msg
            print ady
            print address
            print


def isValidAddress(ady):

    address = usaddress.parse(ady)
    if len(address) < 4:
        showFailureReason('Not Enough Terms', ady, address)
        return False

    if any([a[1] == 'Recipient' for a in address]):
        showFailureReason('Recipient', ady, address)
        return False

    if not any([a[1] == 'StreetName' for a in address]):
        showFailureReason('StreetName', ady, address)
        return False

    if not any([a[1] == 'AddressNumber' for a in address]):
        showFailureReason('AddressNumber', ady, address)
        return False

    # filter out improbable address endings
    last = ady.split(' ')[-1].lower()
    if last in ['food', 'inc', 'corp', 'llc', 'room', 'of']:
        showFailureReason('Bad Ending', ady, address)
        return False

    # print ady
    # print address
    # print
    return True


def parse(text):
    candidates = probableAddresses(text)
    # for c in candidates:
    #     print c

    candidates = [util.location_to_string(c) for c in candidates]
    return [c for c in candidates if isValidAddress(c)]


if __name__ == '__main__':
    import codecs

    sample = codecs.open('trainers/ad-trainer2.txt', 'r', encoding='utf8') \
        .read()

    print parse(sample)

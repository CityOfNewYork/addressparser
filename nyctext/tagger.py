# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"


import re
import os
import nltk
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
from nltk.tokenize import word_tokenize

import preprocess
from neighborhoods import throughway_names


def filter_probable_company(tup):
    rex = re.compile('(inc|rest|corp|llc)\.?', re.IGNORECASE)
    if rex.match(tup[0]):
        return tup[0], '-NONE-'
    return tup


def filter_comma(tup):
    if tup[0] == ',':
        return ',', 'COMMA'
    return tup


def filter_hash(tup):
    if tup[0] == '#':
        return '#', 'HASH'
    return tup


def filter_cd(tup):
    # ls (list marker) is not necessarey, should be a digit
    val, tag = tup[0].lower(), tup[1]
    if tag == 'LS':
        return val, 'CD'
    elif len(val) > 2 and \
            val[-2:] in ['st', 'nd', 'rd', 'th'] and \
            val[0].isdigit() and val[-3].isdigit():
        return tup[0], 'CD'
    # elif val.isdigit():
    #     return tup[0], 'CD'
    return tup


def filter_throughways(tup):
    '''Identify and tag throughway names.

    '''
    # Todo: This alg has to change so that it doesn't
    #       assign 'LU' to portions of a neighborhood-
    #       name...
    #       Consider passing a context object to keep
    #       track of the annotations an address goes through.
    #       it will have which neighborhood was mapped
    #       making it easier to eliminate those LU matches.
    #
    # 1: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html
    # have to treat broadway & bowery as a thhoroughfare
    # because they are valid street names and thoroughfares in of
    # themselves
    rex = re.compile(throughway_names, re.I)

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


def tag_cities(tagged, text):
    r_throughway = re.compile(throughway_names, re.I)
    r_city = re.compile('(manhattan|brooklyn|bronx|queens)', re.I)

    new_tagged = []
    for dx in range(len(tagged)-1):
        cur, nxt = tagged[dx], tagged[dx+1]
        if r_city.match(cur[0]) and not r_throughway.match(nxt[0]):
            new_tagged.append((cur[0], 'CITY'))
        else:
            new_tagged.append(cur)

    last = tagged[-1]
    if r_city.match(last[0]):
        new_tagged.append((last[0], 'CITY'))
    else:
        new_tagged.append(last)

    # handle special case of "staten island", multi word
    if 'staten island' in text.lower():
        tup = None
        for t in new_tagged:
            if t[0].lower() == 'staten':
                tup = t
                break
        dx = new_tagged.index(tup)
        _tagged = [list(t) for t in new_tagged]
        _tagged[dx][1] = 'CITY'
        _tagged[dx+1][1] = 'CITY'
        new_tagged = [tuple(t) for t in _tagged]

    return new_tagged


def transform_tags(tagged, text):
    # retag commas
    tagged = map(filter_comma, tagged)

    # retag #
    tagged = map(filter_hash, tagged)

    # change counting lists (ls) to counting digits (cd)
    tagged = map(filter_cd, tagged)

    # tag street names
    tagged = map(filter_throughways, tagged)

    # tag state
    tagged = map(filter_state, tagged)

    # tag city
    tagged = tag_cities(tagged, text)
    return tagged


def pos_tag(text, verbose=False):
    tokens = word_tokenize(preprocess.prepare_text(text, verbose))
    tagged = nltk.pos_tag(tokens)

    tagged = transform_tags(tagged, text)

    # change POS tag to -NONE- to aid chunking
    # Todo: better comments -- remove this function to find
    # cases where this break tests
    tagged = map(filter_probable_company, tagged)

    # Remove incorrect CITY tags.
    # ie, those not succeeded by STATE
    nopuncts = [[v, k] for v, k in tagged if v not in ['.', ',']]
    for i in range(len(nopuncts)-1):
        j = i+1
        if nopuncts[i][1] == 'CITY' and nopuncts[j][1] not in ["STATE", "CITY"]:
            nopuncts[i][1] = 'NNP'
    nopuncts.reverse()
    _tagged = []
    for v, k in tagged:
        if v in ['.', ',']:
            _tagged.append((v, k))
        else:
            _tagged.append(tuple(nopuncts.pop()))
    tagged = _tagged

    return tagged


def do_chunk(text, verbose=False):

    tagged = pos_tag(text, verbose)
    if verbose:
        print tagged

    # import ipdb;  ipdb.set_trace()
    # infer Street if missing in manhattan
    # addresses
    anchors = [(v, t) for v, t in tagged if t == 'CITY' and v == 'Manhattan']
    streets = [(v, t) for v, t in tagged if t == 'LU']

    if anchors and not streets:

        # find first CD to left
        anc = anchors[0]
        i = tagged.index(anc)
        while i > 0:
            i -= 1
            tag = tagged[i][1]
            if tag == 'LU':
                return tagged
            elif tag == 'CD':
                # insert street
                tagged.insert(i+1, (u'Street', u'LU'))
                return tagged
    return tagged


def chunkAddresses(text, verbose=False):

    tagged = do_chunk(text, verbose)
    grammer = 'Location: ' \
        '{' \
        '<CD>' \
        '<CD|DT|IN|NN|NNP|NNS|JJ|JJS|COMMMA|POS|PRP|HASH|WDT>*' \
        '<LU>+?' \
        '<CD|JJ|IN|JJS|NN|NNP|NNS|COMMA|IN|DT|PRP|HASH|RB|VBP>*' \
        '<CITY>+' \
        '<COMMA>?' \
        '<STATE>' \
        '}'

    chunkParser = nltk.RegexpParser(grammer)
    chunks = chunkParser.parse(tagged)
    locations = [s for s in chunks.subtrees(lambda t: t.label() == 'Location')]
    if verbose:
        print 'Chunked Locations:'
        if locations:
            for loc in locations:
                print '\t', loc
                print
        else:
            print '\tNone found'
    return locations

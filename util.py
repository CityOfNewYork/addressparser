# -*- coding: utf-8 -*-
import re
import historicMappings

_rex_boroughs = re.compile('(in\s+the\s+)Borough\s+of\s+'
                           '(Brooklyn|Queens|Staten\s+Island|Bronx)',
                           re.IGNORECASE)

_rex_manhattan = re.compile('(in\s+the\s+)Borough\s+of\s+'
                            '(Manhattan)',
                            re.IGNORECASE)

# match these...
# BOROUGH OF QUEENS 15-5446-Block 1289, lot 15–
# BOROUGH OF QUEENS 15-7412 - Block 8020, lot 6–
# BOROUGH OF BROOKLYN 15-7494-Block 2382, lot 3–
# BOROUGH OF MANHATTAN 15-6223 – Block 15, lot 22-
_b = '[brooklyn|bronx|manhattan|staten\s+island|queens]'
_rex_blockcodes = r'BOROUGH\s+of\s+%s[^b]+block[^,]+,\s+lot[\s\d]+.' % _b
_rex_blockcodes = re.compile(_rex_blockcodes, re.IGNORECASE)

def filter_boroughs(text):
    global _rex_boroughs, _rex_manhattan
    text = _rex_manhattan.sub('NY, NY.\n', text)
    return _rex_boroughs.sub('\\2, NY.\n', text)


def filter_blockcodes(text):
    global _rex_blockcodes
    return '.\n'.join( [para for para in _rex_blockcodes.split(text)])

def preproces_text(text):
    # replace unicode dash(-) with ascii dash(-)
    text = text.replace(u'\u2013', '-')

    text = filter_boroughs(text)
    text = filter_blockcodes(text)
    return historicMappings.preprocess(text)


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


def showResults(res):
    for ad in res:
        print location_to_string(ad)


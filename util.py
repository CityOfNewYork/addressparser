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
    return '.\n'.join([para for para in _rex_blockcodes.split(text)])


# Entry point for preprocessing. Add more methods within this
# function
def preproces_text(text):
    text = filter_boroughs(text)
    text = filter_blockcodes(text)
    return historicMappings.preprocess(text)


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


#Some filters for other address formats

#For instances such as "22 Reade Street, Spector Hall, Borough of Manhattan"
boroughOf = re.compile(r"""(Borough\s+of\s+)
                           (Brooklyn|Queens|Staten\s+Island|Bronx)""",
                           re.IGNORECASE | re.VERBOSE)

boroughOfManhattan = re.compile(r"""(Borough\s+of\s+)
                           (Manhattan)""",
                           re.IGNORECASE | re.VERBOSE)

def filterBoroughOf(text):
    return re.sub(boroughOf, r"""\g<2>, NY""", text)

def filterBoroughOfManhattan(text):
    return re.sub(boroughOfManhattan, r"""New York, NY""", text)


#For instances such as "1 Centre Street in Manhattan"

inBorough = re.compile(r"""(\sin\s)
                           (Brooklyn|Queens|Staten\s+Island|Bronx)""", 
                           re.IGNORECASE | re.VERBOSE)

inManhattan = re.compile(r"""(\sin\s)
                           (Manhattan)""", 
                           re.IGNORECASE | re.VERBOSE)

def filterInBorough(text):
    return re.sub(inBorough, r', \g<2>, NY', text)

def filterInManhattan(text):
    return re.sub(inManhattan, r', New York, NY', text)

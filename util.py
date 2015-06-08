# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

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
    text = _rex_manhattan.sub('Manhattan, NY.\n', text)
    return _rex_boroughs.sub('\\2, NY.\n', text)


def filter_blockcodes(text):
    global _rex_blockcodes
    return '.\n'.join([para for para in _rex_blockcodes.split(text)])

_street_abreviations = re.compile('\s+(st\.|str\.)[\s,]', re.IGNORECASE)
_avenue_abreviations = re.compile('\s+(av\.|ave\.)[\s,]', re.IGNORECASE)
# _circle_abreviations = re.compile('\s+(cir\.)[\s,]', re.IGNORECASE)


def filter_street_abbreviations(text):
    global _street_abreviations, _avenue_abreviations
    # globa  _circle_abreviations
    text =  _street_abreviations.sub(' Street', text)
    text =  _avenue_abreviations.sub(' Avenue', text)
    # text =  _circle_abreviations.sub(' Circle', text)
    return text

_ny_ny = re.compile('(new\s+york|NY)[\s,]+(new\s+york|NY)\s?', re.IGNORECASE)
def filter_ny_ny(text):
    global _ny_ny
    return  _ny_ny.sub('Manhattan, NY.\n', text)


# Entry point for preprocessing. Add more methods within this
# function
def preproces_text(text, verbose=True):
    # There should be a section of removing all unicode
    # and non ascii characters.
    #
    text = text.replace(u'\xa0', ' ')

    text = filter_boroughs(text)
    if verbose:
        print 'filter_boroughs:\n\t%s\n' % text

    text = filter_ny_ny(text)
    if verbose:
        print 'filter_ny_ny:\n\t%s\n' % text

    text = filter_blockcodes(text)
    if verbose:
        print 'filter_blockcodes:\n\t%s\n' % text

    text = historicMappings.preprocess(text)
    if verbose:
        print 'historicMappings:\n\t%s\n' % text

    text = filter_street_abbreviations(text)
    if verbose:
        print 'filter_street_abbreviations:\n\t%s\n' % text

    return text


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


# Some filters for other address formats

# For instances such as "22 Reade Street, Spector Hall, Borough of Manhattan"
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


# For instances such as "1 Centre Street in Manhattan"

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

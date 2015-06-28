# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

import re
import historicMappings
from queens import rex_neighborhoods_queens
from brooklyn import rex_neighborhoods_brooklyn
from bronx import rex_neighborhoods_bronx
from statenisland import rex_neighborhoods_statenIsland
from manhattan import rex_neighborhoods_manhattan

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


_street_abbreviations = re.compile('\s+(st\.|str\.)[\s,]', re.IGNORECASE)
_avenue_abbreviations = re.compile('\s+(av\.|ave\.)[\s,]', re.IGNORECASE)


def filter_street_abbreviations(text):
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html

    global _street_abbreviations, _avenue_abbreviations
    text = _street_abbreviations.sub(' Street', text)
    text = _avenue_abbreviations.sub(' Avenue', text)
    return text


_ny_ny = re.compile('(new\s+york|NY)[\s,]+(new\s+york|NY)\s?', re.IGNORECASE)


def filter_ny_ny(text):
    global _ny_ny
    return _ny_ny.sub('Manhattan, NY.\n', text)


def filter_neighborhoods(text):
    _t = text.lower()
    if 'queens' not in _t:
        text = rex_neighborhoods_queens.sub('\\1, Queens,', text)

    if 'brooklyn' not in _t:
        text = rex_neighborhoods_brooklyn.sub('\\1, Brooklyn,', text)

    if 'staten island' not in _t:
        text = rex_neighborhoods_statenIsland.sub('\\1, Staten Island,', text)

    # skip if 'NY, NY' in expression
    if 'manhattan' not in _t and 'ny, ny' not in _t:
        text = rex_neighborhoods_manhattan.sub('\\1, Manhattan,', text)

    # Marble Hill can be both manhattan and bronx
    if 'marble hill' not in _t and 'bronx' not in _t:
        text = rex_neighborhoods_bronx.sub('\\1, Bronx,', text)
    text = text.replace(',,', ',')
    return text


# Entry point for preprocessing. Add more methods within this
# function
def prepare_text(text, verbose=False):
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

    text = filter_neighborhoods(text)
    if verbose:
        print 'filter_neighborhoods:\n\t%s\n' % text

    return text


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


# Some filters for other address formats
# For instances such as "22 Reade Street, Spector Hall, Borough of Manhattan"
# boroughOf = re.compile(r"""(Borough\s+of\s+)
#                            (Brooklyn|Queens|Staten\s+Island|Bronx)""",
#                            re.IGNORECASE | re.VERBOSE)
#
# boroughOfManhattan = re.compile(r"""(Borough\s+of\s+)
#                            (Manhattan)""",
#                            re.IGNORECASE | re.VERBOSE)
#
# def filterBoroughOf(text):
#     return re.sub(boroughOf, r"""\g<2>, NY""", text)
#
# def filterBoroughOfManhattan(text):
#     return re.sub(boroughOfManhattan, r"""New York, NY""", text)
#
#
# # For instances such as "1 Centre Street in Manhattan"
#
# inBorough = re.compile(r"""(\sin\s)
#                            (Brooklyn|Queens|Staten\s+Island|Bronx)""",
#                            re.IGNORECASE | re.VERBOSE)
#
#
# inManhattan = re.compile(r"""(\sin\s)
#                            (Manhattan)""",
#                            re.IGNORECASE | re.VERBOSE)
#
#
# def filterInBorough(text):
#     return re.sub(inBorough, r', \g<2>, NY', text)
#
#
# def filterInManhattan(text):
#     return re.sub(inManhattan, r', New York, NY', text)

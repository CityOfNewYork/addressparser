# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

import re
import historicMappings

from neighborhoods import rex_neighborhoods_queens
from neighborhoods import rex_neighborhoods_brooklyn
from neighborhoods import rex_neighborhoods_bronx
from neighborhoods import rex_neighborhoods_statenIsland
from neighborhoods import rex_neighborhoods_manhattan
from neighborhoods import throughways
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


_street_abbreviations = re.compile('\s+(str?\.?)[\s,]', re.IGNORECASE)
_avenue_abbreviations = re.compile('\s+(ave?\.?)[\s,]', re.IGNORECASE)
_boulevard_abbreviations = re.compile('\s+(blvd?\.?)[\s,]', re.IGNORECASE)
_plaza_abbreviations = re.compile('\s+(plz?\.?)[\s,]', re.IGNORECASE)
_drive_abbreviations = re.compile('\s+(dr?\.?)[\s,]', re.IGNORECASE)
_parkway_abbreviations = re.compile('\s+(pkwy?\.?)[\s,]', re.IGNORECASE)
_road_abbreviations = re.compile('\s+(rd\.?)[\s,]', re.IGNORECASE)


def filter_street_abbreviations(text):
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html

    global _street_abbreviations, _avenue_abbreviations
    text = _street_abbreviations.sub(' Street ', text)
    text = _avenue_abbreviations.sub(' Avenue ', text)
    text = _boulevard_abbreviations.sub(' Boulevard ', text)
    text = _plaza_abbreviations.sub(' Plaza ', text)
    text = _drive_abbreviations.sub(' Drive ', text)
    text = _parkway_abbreviations.sub(' Parkway ', text)
    text = _road_abbreviations.sub(' Road ', text)
    return text


_ny_ny = re.compile('(new\s+york|NY)[\s,]+(new\s+york|NY)\s?', re.IGNORECASE)


def filter_ny_ny(text):
    global _ny_ny
    return _ny_ny.sub('Manhattan, NY.\n', text)


def filter_neighborhoods(text):
    text = rex_neighborhoods_queens.sub(', \\1, Queens,', text)

    text = rex_neighborhoods_brooklyn.sub(', \\1, Brooklyn,', text)

    text = rex_neighborhoods_statenIsland.sub(', \\1, Staten Island,', text)

    text = rex_neighborhoods_manhattan.sub(', \\1, Manhattan,', text)

    # Marble Hill can be both manhattan and bronx
    # if not _bronx.match(_t):
    # if 'marble hill' not in _t and 'bronx' not in _t:
    text = rex_neighborhoods_bronx.sub(', \\1, Bronx,', text)

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

    text = filter_neighborhoods(text)
    if verbose:
        print 'filter_neighborhoods:\n\t%s\n' % text

    text = filter_street_abbreviations(text)
    if verbose:
        print 'filter_street_abbreviations:\n\t%s\n' % text

    return text


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')

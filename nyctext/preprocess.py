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


def filter_boroughs(text):
    _rex_boroughs = re.compile('(in\s+the\s+)Borough\s+of\s+'
                               '(Brooklyn|Queens|Staten\s+Island|Bronx)',
                               re.I)

    _rex_manhattan = re.compile('(in\s+the\s+)Borough\s+of\s+'
                                '(Manhattan)',
                                re.I)
    text = _rex_manhattan.sub('Manhattan, NY.\n', text)
    return _rex_boroughs.sub('\\2, NY.\n', text)


def filter_blockcodes(text):
    # match these...
    # BOROUGH OF QUEENS 15-5446-Block 1289, lot 15–
    # BOROUGH OF QUEENS 15-7412 - Block 8020, lot 6–
    # BOROUGH OF BROOKLYN 15-7494-Block 2382, lot 3–
    # BOROUGH OF MANHATTAN 15-6223 – Block 15, lot 22-
    _b = 'brooklyn|bronx|manhattan|staten\s+island|queens'
    _rex_blockcodes = "BOROUGH\s+of\s+(%s)\s+[^b]{7,15}Block\s+\d+,\slot\s\d+.\s*" % _b
    _rex_blockcodes = re.compile(_rex_blockcodes, re.I)

    return '.\n'.join([para for para in _rex_blockcodes.split(text)])


def filter_ny_ny(text):
    _ny_ny = r"\b((new\s*york|ny)\b[\s,]*)\b(new\s*york|ny)\b"
    _ny_ny = re.compile(_ny_ny, re.I)
    return _ny_ny.sub('Manhattan, NY.\n', text)


def filter_neighborhoods(text):
    text = rex_neighborhoods_queens.sub(', \\1, Queens, ', text)

    text = rex_neighborhoods_brooklyn.sub(', \\1, Brooklyn, ', text)

    text = rex_neighborhoods_statenIsland.sub(', \\1, Staten Island, ', text)

    text = rex_neighborhoods_manhattan.sub(', \\1, Manhattan, ', text)

    # Marble Hill can be both manhattan and bronx
    # if not _bronx.match(_t):
    # if 'marble hill' not in _t and 'bronx' not in _t:
    text = rex_neighborhoods_bronx.sub(', \\1, Bronx, ', text)

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

    return text

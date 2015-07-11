# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"



import os
import unicodedata
import nltk
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
from nltk.tokenize import sent_tokenize

import re

import usaddress

from schema import RefLocation
from tagger import chunkAddresses
from pretokenize import transform


def showFailureReason(msg, address, components, verbose=False):
    if verbose:
        print 'Failed: %s' % msg
        print '\tAddress:\t\t%s' % address
        print '\tUS Address Components:\t%s\n' % components


def location_to_string(tree):
    txt = ' '.join([c[0] for c in tree]).replace(' ,', ',')

    # Handle chunked: 600 St Ann's Avenue Bronx, NY
    # (Location 600/CD Saint/NNP Ann/NNP 'S/POS Avenue/LU Bronx/NNP
    # ,/COMMA NY/STATE) by removing space before appostrophe
    return txt.replace(" '", "'")


def matchAddresses(text, verbose=False):
    locations = []
    # Replace periods where it is preceeded by a single
    # Letter
    #
    text = transform(text, verbose=verbose)

    sentences = sent_tokenize(text)
    for s in sentences:
        # s = transform(s, verbose=verbose)

        if verbose:
            print '\n\n'
            print '=' * 48
            print 'Sentence: %s\n' % s

        if verbose:
            print 'Stripping White Spaces:\n\t%s\n' % s
        s = re.sub('\s+', ' ', s)
        if len(s) < 10:
            if verbose:
                showFailureReason('Sentence too short', s, '--', verbose)
            continue
        locs = chunkAddresses(s, verbose)
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
        dic = {}
        for v, k in address:
            dic[k] = '%s %s' % (dic.get(k, ''), v)

        if 'BuildingName' in dic and 'PlaceName' in dic and \
           'StateName' in dic:
            return True

        showFailureReason('StreetName', ady, address, verbose)
        return False

    if not any([a[1] == 'AddressNumber' for a in address]):
        showFailureReason('AddressNumber', ady, address, verbose)
        return False

    return True


def lookup_geo(g, ady, verbose=False):
    if verbose:
        print 'Lookup_geo:\n\t%s' % ady

    tags, _ = usaddress.tag(ady)

    addressNumber = tags.get('AddressNumber', '')
    streetName = [v for k, v in tags.items() if k.startswith('StreetName')]
    streetName = ' '.join(streetName)
    borough = tags.get('PlaceName', '').lower()

    if 'ny' in borough or 'manhattan' in borough:
        borough = 'manhattan'

    if 'queens' in borough:
        borough = 'queens'

    if 'brooklyn' in borough:
        borough = 'brooklyn'

    if 'bronx' in borough:
        borough = 'bronx'

    if 'manhattan' in borough:
        borough = 'manhattan'

    if 'staten island' in borough:
        borough = 'staten island'

    if verbose:
        print usaddress.tag(ady)
        print 'adNumber: %s\t\tstName: %s\t\tBorough:%s\n\n' % (addressNumber,
                                                                streetName,
                                                                borough)

    dic = g.address(addressNumber, streetName, borough)
    zipcode = dic.get('zipCode', '')
    streetAddress = '%s %s' % (dic.get('houseNumber', ''),
                               dic.get('firstStreetNameNormalized', ''))

    borough = dic.get('firstBoroughName', '')
    longitude = dic.get('longitude', '')
    latitude = dic.get('latitude', '')

    place = RefLocation(streetAddress, borough, zipcode, latitude, longitude)
    return place.schema_object()

def normalize_text(text):
    'Remove accents and other annotations from unicode characters'
    return unicodedata.normalize(
              'NFKD', 
              text.decode('utf8', 'strict')).encode('ascii', 'ignore')

def parse(text, verbose=False):
    text = normalize_text(text)
    candidates = matchAddresses(text, verbose)
    candidates = [location_to_string(c) for c in candidates]

    # only candidates that end in NY
    rex = re.compile('(.+\s+NY)', re.IGNORECASE)
    candidates = [rex.match(c) for c in candidates]
    candidates = [c.group() for c in candidates if c is not None]
    return [c for c in candidates if isValidAddress(c, verbose)]


def parse_with_geo(text, g, verbose=False):
    plains = parse(text, verbose)
    return [lookup_geo(g, p, verbose) for p in plains]

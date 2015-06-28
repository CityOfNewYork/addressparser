# -*- coding: utf-8 -*-
from os import environ
import codecs
import os.path
import sys
sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from nyc_geoclient import Geoclient

from nyctext import nycaddress as parser
# import highschools_dic
import pprint


# Address with multiple LUs doesn't get chunked properly
# 'Bronx Engineering and Technology Academy: 99 Terrace View Avenue Bronx, NY'

class Address:

    def __init__(self, source, verbose=False):
        # import ipdb; ipdb.set_trace()
        self.source = source
        self.address = parser.parse(source, verbose=verbose)
        if self.address:
            self.address = self.address[0]

    def asDict(self):
        return dict(address=self.address, source=self.source)

def bad_addresses():
    return '''Academy of Innovative Technology: 999 Jamaica Avenue Brooklyn, NY
Brooklyn Lab School: 999 Jamaica Avenue Brooklyn, NY
Central Park East High School: 1573 Madison Avenue New York, NY
Multicultural High School: 999 Jamaica Avenue Brooklyn, NY
The Urban Assembly School for Global Commerce: 2005 Madison Avenue New York, NY
'''.split('\n')[:-1]

def main():
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)

    lines = codecs.open('data/highschools.txt', encoding='latin1').read()
    lines = lines.split('\n')
    lines = bad_addresses()
    entries = [Address(l, verbose=False).asDict()
               for l in lines if l.strip() != '']
    # for entry in entries:
    #     entry['geo'] = parser.parse_with_geo(entry['source'], g, verbose=False)

    for entry in entries:
        # if entry['address'] != []: continue
        pprint.pprint(entry, indent=2)
        print
        # print entry['source']

if __name__ == '__main__':
    main()

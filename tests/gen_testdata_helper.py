# -*- coding: utf-8 -*-
from os import environ
import codecs
import os.path
import sys
sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from nyc_geoclient import Geoclient
from nyctext import nycaddress as parser
import json


# Address with multiple LUs doesn't get chunked properly
# 'Bronx Engineering and Technology Academy: 99 Terrace View Avenue Bronx, NY'

class Address:

    def __init__(self, source, verbose=False):
        self.source = source
        self.address = parser.parse(source, verbose=verbose)
        if self.address:
            self.address = self.address[0]
        else:
            self.address = None

    def asDict(self):
        return dict(address=self.address, source=self.source)

    def __str__(self):
        # return '{ "address": "%s",\n "source": "%s"\n}' % (self.address, self.source)
        return json.dumps(self.asDict(), indent=1)


def bad_addresses():
    return '''Academy of Innovative Technology: 999 Jamaica Avenue Brooklyn, NY
Brooklyn Lab School: 999 Jamaica Avenue Brooklyn, NY
Central Park East High School: 1573 Madison Avenue New York, NY
Multicultural High School: 999 Jamaica Avenue Brooklyn, NY
The Urban Assembly School for Global Commerce: 2005 Madison Avenue New York, NY
'''.split('\n')[:-1]

def lines():

    # files = ['data/ACRIS_-_Personal_Property_Parties.txt',
    files = [
             'data/DOHMH_New_York_City_Restaurant_Inspection_Results.txt',
             'data/Lower_Manhattan_Retailers.txt',
             'data/Mapped_In_NY_Companies.txt']


    for fn in files:
        count = 1000
        with codecs.open(fn, encoding='latin1') as dataset:
            for line in dataset:
                line = line.strip()
                if line == '':
                    continue
                count -= 1
                if count < 1:
                    break
                yield line

def processAll(g):
    unparsed, parsed = 0, 0
    for line in lines():
        if line.strip() == '':
            continue
        ad = Address(line, verbose=False)
        if ad.address is None:
            unparsed += 1
            print 'source: %s' % ad.source


    print '\n\nSummary Unparsed: %d' % unparsed



def processAdys(g, fn):
    lines = codecs.open(fn, encoding='latin1').read()
    lines = lines.split('\n')
    entries = [Address(l, verbose=False) for l in lines if l.strip() != '']
# for entry in entries:
#     entry['geo'] = parser.parse_with_geo(entry['source'], g, verbose=False)

    unparsed, parsed = [], []

    for e in entries:
        if e.address:
            parsed.append(e.asDict())
        else:
            unparsed.append(e.asDict())

    print '%d Unparsed Addresses' % (len(unparsed))
    print '%d Parsed Addresses' % (len(parsed))
    for e in  unparsed:
        print 'source: "%s"' % e['source']
        # print Address(e['source'], verbose=True)
        # print '\n'*3

    # print json.dumps(unparsed, indent=1)





if __name__ == '__main__':
    fn = 'data/Lower_Manhattan_Retailers.txt'
    fn =  'data/Mapped_In_NY_Companies.txt'
    # import ipdb; ipdb.set_trace()
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)
    # processAdys(g, fn)
    processAll(g)

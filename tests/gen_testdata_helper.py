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

    files = ['data/ACRIS_-_Personal_Property_Parties.txt',
             'data/DOHMH_New_York_City_Restaurant_Inspection_Results.txt',
             'data/Lower_Manhattan_Retailers.txt',
             'data/Mapped_In_NY_Companies.txt',
             'data/highschools.txt',
             ]


    for fn in files:
        count = 5000
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
    nUnparsed, nParsed = 0, 0
    unparsed, parsed = [], []
    dic = []
    for line in lines():
        if line.strip() == '':
            continue
        ad = Address(line, verbose=False)
        if ad.address is None:
            dic.append(dict(parsed=False, text=line))
            unparsed.append(line)
            nUnparsed += 1
        else:
            dic.append(dict(parsed=True, text=line))
            parsed.append(line)
            nParsed += 1

    print '\n\nSummary:\n\tUnparsed: %d\n\tParsed: %d' % (nUnparsed, nParsed)
    total = 1.0*(nParsed + nUnparsed)
    print 'Completion %%: %f' % (nParsed/total*100)

    f_parsed = codecs.open('ad-pass.txt', 'w', 'utf-8')
    f_unparsed = codecs.open('ad-fail.txt', 'w', 'utf-8')
    print 'Writing outputs'
    for line in parsed:
        f_parsed.write('%s\n' % line)

    for line in unparsed:
        f_unparsed.write('%s\n' % line)
    f_parsed.flush()
    f_unparsed.flush()


if __name__ == '__main__':
    fn = 'data/Lower_Manhattan_Retailers.txt'
    fn =  'data/Mapped_In_NY_Companies.txt'
    # import ipdb; ipdb.set_trace()
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)
    # processAdys(g, fn)
    processAll(g)

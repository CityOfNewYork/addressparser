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


class Address:

    def __init__(self, source, verbose=False):
        # import ipdb; ipdb.set_trace()
        self.source = source
        self.address = parser.parse(source, verbose=verbose)
        print 'Address: %s' % self.address
        if self.address:
            self.address = self.address[0]

    def asDict(self):
        return dict(address=self.address, source=self.source)


def main():
    lines = codecs.open('data/highschools.txt', encoding='latin1').read()
    lines = lines.split('\n')
    lines = [
u'''DESIGN AND CONSTRUCTION  PUBLIC HEARINGS PLEASE TAKE NOTICE, that in
accordance with Section 201-204 (inclusive) of the New York State Eminent Domain
Procedure Law (“EDPL”), a public hearing will be held by the New York City
Department of Design and Construction, on behalf of the City of New York in
connection with the acquisition of certain properties for the construction of
sanitary and storm sewers, water mains and appurtenances in Grantwood Avenue
between Sheldon Avenue and Rensselaer Avenue; Grantwood Avenue between
Rensselaer Avenue and Rathbun Avenue and the intersection of Sheldon and
Belfield Avenues (Capital Project No. SER200196) – Borough of Staten Island. The
time and place of the hearing is as follows: Date: April 21, 2015 Time: 10:00
A.M. Location: Community Board No. 3 Woodrow Plaza 655 Rossville Avenue Staten
Island, NY 10309 The purpose of this hearing is to inform the public of the
proposed acquisition of certain street beds and to review the public use to be
        '''
    ]
    entries = [Address(l, verbose=True).asDict() for l in lines if l.strip() !=
               '' and 'staten island' in l.lower()]
    # entries = [Address(l,verbose=True).asDict() for l in lines]
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)
    pprint.pprint(entries)
    # pprint.pprint(parser.parse_with_geo(lines[0],g,verbose=True))
    for entry in entries:
        entry['geo'] = parser.parse_with_geo(entry['source'], g, verbose=True)
        pprint.pprint(entry)

if __name__ == '__main__':
    main()

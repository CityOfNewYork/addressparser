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
    # lines = [
    # ]
    entries = [Address(l,verbose=True).asDict() for l in lines if l.strip() != '' and 'bronx' in l.lower()]
    # entries = [Address(l,verbose=True).asDict() for l in lines]
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)
    pprint.pprint(entries)
    # pprint.pprint(parser.parse_with_geo(lines[0],g,verbose=True))
    for entry in entries:
        entry['geo'] = parser.parse_with_geo(entry['source'], g)
        pprint.pprint(entry)

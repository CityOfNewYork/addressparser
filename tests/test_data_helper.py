import codecs
import os.path
import sys
sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))


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


lines = codecs.open('data/highschools.txt', encoding='latin1').read()
lines = lines.split('\n')
entries = [Address(l).asDict() for l in lines if l.strip() != '' and 'queens' in l.lower()]

pprint.pprint(entries)
# for entry in entries:
#     pprint.pprint(entry)

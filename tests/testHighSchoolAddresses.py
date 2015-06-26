import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest
import codecs
import re

from nyctext import nycaddress as parser

@SkipTest
class HighSchools(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(HighSchools, self).__init__(*args, **kwds)
        self.cwd = os.path.dirname(__file__)
        # extract list of addresses
        text = open(os.path.join(self.cwd, 'data', 'highschools.txt')).readlines()
        self.reg_ny = re.compile('New York, NY', re.I)
        self.addresses = [self.normalize(l.split(':')[-1].strip()) for l in text]


    def normalize(self, ad):
        return self.reg_ny.sub('Manhattan, NY', ad)


    def checkExpectation(self, source, verbose=False):
        addresses = parser.parse(source, verbose)
        for loc in addresses:
            # self.assertIn(loc, self.addresses)
            if loc in self.addresses:
                self.addresses.remove(loc)
            else:
                print 'Unverifiable Parsed Addres: %s' % loc

        print 'Address not discovered'
        for ad in self.addresses:
            print ad
        self.assertEqual(self.addresses, [])


    @attr(type="wip")
    def testFoo(self):
        source =  open(os.path.join(self.cwd, 'data', 'highschools.txt')).read().decode('latin1')
        self.checkExpectation(source)


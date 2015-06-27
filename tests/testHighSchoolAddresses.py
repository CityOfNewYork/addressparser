import os.path
import sys
sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import unittest

from nyctext import nycaddress as parser
import highschools_dic


class HighSchools(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(HighSchools, self).__init__(*args, **kwds)
        self.samples = highschools_dic.samples

    # def normalize(self, ad):
    #     return self.reg_ny.sub('Manhattan, NY', ad)

    def checkExpectation(self, verbose=False):
        for d in self.samples:
            got = parser.parse(d['text'], verbose)
            if got:
                got = got[0]
            exp = d['address']
            if got != exp:
                print '%s\n\t%s\n\t%s\n\n' % (got, exp, d)

    @attr(type="wip")
    def testFoo(self):
        self.checkExpectation(False)

import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest

from nyctext import nycaddress as parser


class WithOccupancy(unittest.TestCase):
    '''Addresses with Occupancy tags
    '''

    def checkExpectation(self, source, expected, verbose=False):
        addresses = parser.parse(source, verbose)
        if verbose:
            print 'source: %s' % source
            print 'expected: %s' % expected
            print 'got: %s' % addresses
        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)
        self.assertEqual(expected, [])

    def testHandleFloor_flr_period(self):
        'process addresses with floor (flr.)'

        source = "DoSomething.org: 19 West 21st St, 8th Flr. , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_flr(self):
        'process addresses with floor (flr)'

        source = "DoSomething.org: 19 West 21st St, 8th Flr, New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_fl_period(self):
        'process addresses with floor (flr.)'

        source = "DoSomething.org: 19 West 21st St, 8th Fl. , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_fl(self):
        'process addresses with floor (flr)'

        source = "DoSomething.org: 19 West 21st St, 8th Fl , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

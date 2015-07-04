import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest

from nyctext import nycaddress as parser


class PeriodManipulation(unittest.TestCase):
    '''Add description HERE
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

    def testPeriodBetweenNNPAndThroughfare(self):
        'wipe out the following period: NNP . LU'


        names = [
            'avenue', 'boulevard',
            'broadway', 'circle', 'crescent',
            'drive', 'expressway', 'highway',
            'lane', 'park', 'piers',
            'place', 'plaza', 'road',
            'slip', 'square', 'street',
            'terrace', 'turnpike'
        ]
        for name in names:
            source = "65 Greene. %s 4th Floor, New York, NY" % name
            expected = "65 Greene %s 4th Floor, Manhattan, NY" % name
            expected = [expected]

            self.checkExpectation(source, expected)

import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest

from nyctext import nycaddress as parser


class CityAbbreviations(unittest.TestCase):
    '''Expand city abbreviations
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

    def testManhttan(self):
        'test manhttan'

        source = "CHARLES B. MANUELJR: 237  PARK AVENUE  MANHTTAN, NY"
        expected = "237 PARK AVENUE Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testNewYorkCity(self):
        'test New York City'

        source = "CHARLES B. MANUELJR: 237  PARK AVENUE  New York City, NY"
        expected = "237 PARK AVENUE Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testBrooklynExpands(self):
        'various brooklyn abbreviations expand'
        source = """
            9002  FIFTH AVE  BKYLN, NY.
            100  WOODRUFF AVE  BROOLKYN, NY.
            258  UNION ST  BK, NY.
        """
        expected = [
            "9002 FIFTH Avenue Brooklyn, NY",
            "100 WOODRUFF Avenue Brooklyn, NY",
            "258 UNION Street Brooklyn, NY"
        ]

        self.checkExpectation(source, expected)

    def testBronxExpands(self):
        'various bronx abbreviations expand'
        source = "12  WEST BURNSIDE AVE  BX, NY"
        expected = "12 WEST BURNSIDE Avenue Bronx, NY"
        expected = [expected]
        self.checkExpectation(source, expected)

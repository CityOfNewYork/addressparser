import sys
sys.path.append('..')
import pytest
import os.path
import unittest

from nyctext import nycaddress as parser


class Address(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(Address, self).__init__(*args, **kwds)
        self.cwd = os.path.dirname(__file__)

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

    def testBasicStreet(self):
        'basic - street avenue place plaza boulevard'

        lus = 'street avenue place plaza boulevard'.split(' ')
        template = '12 Fleet %s Manhattan, NY'
        for lu in lus:
            source = template % lu
            self.checkExpectation(source, [source])

    def testWithNumberStreet(self):
        'basic - with numbered street'

        lus = 'street avenue place plaza boulevard'.split(' ')
        template = '123 11 %s Manhattan, NY'
        for lu in lus:
            source = template % lu
            self.checkExpectation(source, [source])

    def testWithNumberStreetAndEnding(self):
        'basic - with numbered street and -st ending'

        lus = 'street avenue place plaza boulevard'.split(' ')
        template = '123 1st %s Manhattan, NY'
        for lu in lus:
            source = template % lu
            self.checkExpectation(source, [source])

    def testWithNumberStreetWithDash(self):
        'basic - with numbered street and dash'

        lus = 'street avenue place plaza boulevard'.split(' ')
        template = '123-45 Acacia %s Manhattan, NY'
        for lu in lus:
            source = template % lu
            self.checkExpectation(source, [source])

    def testWithCompassDirections(self):
        'basic - with compass directions'

        lus = 'street avenue place plaza boulevard'.split(' ')
        points = 'E W S N'.split(' ')
        template = '12 %s Fordham %%s Bronx, NY'
        x_template = '12 %s Fordham %%s Bronx, NY'
        for pt in points:
            tp = template % pt
            xt = x_template % pt
            for lu in lus:
                source = tp % lu
                expect = [xt % lu]
                self.checkExpectation(source, expect)

    def testWithNumberStreetWithDashAndRoom(self):
        'basic - test with dash and Room'

        lus = 'street avenue place plaza boulevard'.split(' ')
        template = '100 Gold %s, Room 5-O8, New York, NY'
        x_template = '100 Gold %s, Room 5-O8, Manhattan, NY'
        for lu in lus:
            source = template % lu
            expect = [x_template % lu]
            self.checkExpectation(source, expect, verbose=True)

    def testIT(self):
        'basic - long island city '

        source = '''30-30 Thomson Avenue Long Island City, NY 11101 '''
        expect = ['30-30 Thomson Avenue, Long Island City, Queens, NY']
        self.checkExpectation(source, expect)

    def testNYNY(self):
        'basic -  NYNY'

        source = '55 Water Street, 9th Floor SW, New York, NY 10041'
        expect = ['55 Water Street, 9th Floor SW, Manhattan, NY']
        self.checkExpectation(source, expect)

    def testSaintAnneAvenue(self):
        'name with apostrophe'
        expected = [u"600 Saint Ann's Avenue Bronx, NY"]
        text = "Academy of Science: 600 Saint Ann's Avenue Bronx, NY"
        address = parser.parse(text)[0]
        self.assertIn(address, expected)

    def testStreetNamePreTypeAveOfAmericas(self):
        'find Avenue of the Americas'
        expected = "131 Avenue Of The Americas Manhattan, NY"
        text = 'blab blah bleu %s foo fe hu' % expected

        got = parser.parse(text)
        self.assertIn(got[0], [expected])

    def testStreetNamePreTypes(self):
        'test Avenue xxx'
        expected = [
            "1600 Avenue L Brooklyn, NY",
            "3000 Avenue X Brooklyn, NY",
            "50 Avenue X Brooklyn, NY"
        ]

        for text in expected:
            text = 'blab blah bleu %s foo fe hu' % text
            got = parser.parse(text)[0]
            self.assertIn(got, expected)

    def testAddressWithMultipleCity(self):
        'test ... Queens, NY  NY, NY finds first address'

        text = "11 W. 19th Street, NY, NY 10011 , New York, NY"
        expected = "11 W 19th Street, Manhattan, NY"
        got = parser.parse(text)[0]
        self.assertEqual(expected, got)

    def testHighwayAbbreviations(self):
        'hwy, expy'
# 3 IN 1 KITCHEN: 4902 FORT HAMILTON PARKWAY BROOKLYN, NY
        text = "238 KINGS HWY BROOKLYN, NY"
        expected = "238 KINGS Highway BROOKLYN, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

        text = "3050 WHITESTONE EXPY QUEENS, NY"
        expected = "3050 WHITESTONE Expressway QUEENS, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

    def testAptAndSuite(self):
        'handle ste and apt'

        text = "35 WEST 89TH STREET APT. 1A NEW YORK, NY"
        expected = "35 WEST 89TH STREET Apt 1A Manhattan, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

        text = "35 WEST 89TH STREET STE. 1A NEW YORK, NY"
        expected = "35 WEST 89TH STREET Suite 1A Manhattan, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

    def testInferredStreet(self):
        'infer street in manhattan'
        text = "10 W 15th , New York, NY"
        expected = "10 W 15th Street, Manhattan, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

    def testPeriodBetweenDirectionAndStreet(self):
        'period handled between direction and street'
        text = "Decker Design: 14W.23rd Street 3rd Floor, New York, NY"
        expected = "14 W 23rd Street 3rd Floor, Manhattan, NY"
        got = parser.parse(text)[0]
        self.assertEqual(got, expected)

    @pytest.mark.skipif("True")
    def testSaintNotStreet(self):
        #This is unimplemented
        '701 St. Anns should resolve to Saint Anns instead of Street Anns'
        expected = ['701 St. Anns Avenue Bronx, NY']

        for text in expected:
            print text
            text = 'blab blah bleu %s foo fe hu' % text
            got = parser.parse(text, verbose=True)[0]
            self.assertIn(got, expected)

    def testInitials(self):

        text = '''
            1180 Reverend J.A. Polite Ave. Bronx, NY.
        '''

        expected = [
            '1180 Reverend J A Polite Avenue Bronx, NY'
        ]

        got = parser.parse(text)[0]
        self.assertIn(got, expected)

    def testColumbusCircle(self):
        'basic -  Columbus Circle'

        lus = 'Circle Cir. Cir'.split(' ')
        for lu in lus:
            source = '4 Columbus %s NY, NY' % lu
            expect = ['4 Columbus Circle Manhattan, NY']
            self.checkExpectation(source, expect, True)

# -*- coding: utf-8 -*-
import sys
sys.path.append('..')


from nose.plugins.skip import SkipTest
# from nose.plugins.attrib import attr
import unittest

from nyctext import nycaddress as parser

class Neighborhoods(unittest.TestCase):


    @SkipTest
    def testHistoricNeighborhoods(self):
        'parse historic marked queens neighborhoods'

        text = u'''CERTIFICATE OF APPROPRIATENESS
        BOROUGH OF QUEENS 14-8118-Block 8041, lot 47-
        121 Arleigh Road-Douglaston Historic District'''

        expect = '121 Arleigh Road, Douglaston Queens, NY'
        got = parser.parse(text, True)[0]
        self.assertEqual(got, expect)

    @SkipTest
    def testQueensNeighborhoods(self):
        'parse queens neighborhoods'
        text = '121 Arleigh Road-Douglaston Historic District'
        expect = '121 Arleigh Road, Douglaston Queens, NY'
        got = parser.parse(text)[0]
        self.assertEqual(got, expect)

    def testNoMappingOnPostConditions(self):
        'Neighborhood + |N|S|W|E|NORTH|SOUTH|EAST|WEST ok'

        directions = 'North South East West N S E W'.split(' ')
        for d in directions:
            text = "19 Union Square %s , New York, NY" % d
            expected = "19 Union Square %s, Manhattan, NY" % d
            expected = [expected]
            got = parser.parse(text)
            self.assertEqual(got, expected)

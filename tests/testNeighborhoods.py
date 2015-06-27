# -*- coding: utf-8 -*-
import sys
sys.path.append('..')


from nose.plugins.skip import SkipTest
# from nose.plugins.attrib import attr
import unittest

from nyctext import nycaddress as parser

@SkipTest
class Neighborhoods(unittest.TestCase):

    def testHistoricNeighborhoods(self):
        'parse historic marked queens neighborhoods'

        text = u'''CERTIFICATE OF APPROPRIATENESS
        BOROUGH OF QUEENS 14-8118-Block 8041, lot 47–
        121 Arleigh Road-Douglaston Historic District'''

        expect = '121 Arleigh Road, Queens, NY'
        got = parser.parse(text, True)[0]
        self.assertEqual(got, expect)

    def testQueensNeighborhoods(self):
        'parse queens neighborhoods'
        text = '121 Arleigh Road-Douglaston Historic District'
        expect = '121 Arleigh Road, Queens, NY'
        got = parser.parse(text)[0]
        self.assertEqual(got, expect)

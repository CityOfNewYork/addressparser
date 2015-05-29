import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
import os.path
import unittest
import codecs

import nycaddress as parser


class PublicHearing(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(PublicHearing, self).__init__(*args, **kwds)
        self.cwd = os.path.dirname(__file__)

    def checkExpectation(self, sample, expect):
        source = os.path.join(self.cwd, sample)
        expectation = os.path.join(self.cwd, expect)

        expected = open(expectation).readlines()
        expected = [e.strip() for e in expected]

        text = codecs.open(source, 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        for loc in addresses:
            print loc
            self.assertIn(loc, expected)
            expected.remove(loc)

        self.assertEqual(expected, [])

    def testDesignAndConstruction(self):
        self.checkExpectation('ad-sample1.txt', 'ad-expected1.txt')

    def testDepartmentOfConsumerAffairs(self):
        self.checkExpectation('ad-sample2.txt', 'ad-expected2.txt')

    def testDepartmentOfTransportation(self):
        self.checkExpectation('ad-sample3.txt', 'ad-expected3.txt')

    def testLandmarkPreservation(self):
        self.checkExpectation('ad-sample4.txt', 'ad-expected4.txt')

import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
import os.path
import unittest
import codecs

import adyparser as parser


class PublicHearing(unittest.TestCase):

    def checkExpectation(self, source, expectation):
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
        source = os.path.join(os.path.dirname(__file__), 'ad-sample1.txt')
        expectation = os.path.join(os.path.dirname(__file__), 'ad-expected1.txt')
        self.checkExpectation(source, expectation)


    def testDepartmentOfConsumerAffairs(self):
        source = os.path.join(os.path.dirname(__file__), 'ad-sample2.txt')
        expectation = os.path.join(os.path.dirname(__file__), 'ad-expected2.txt')
        self.checkExpectation(source, expectation)

    def testDepartmentOfTransportation(self):
        source = os.path.join(os.path.dirname(__file__), 'ad-sample3.txt')
        expectation = os.path.join(os.path.dirname(__file__), 'ad-expected3.txt')
        self.checkExpectation(source, expectation)


    def testLandmarkPreservation(self):
        source = os.path.join(os.path.dirname(__file__), 'ad-sample4.txt')
        expectation = os.path.join(os.path.dirname(__file__), 'ad-expected4.txt')
        self.checkExpectation(source, expectation)


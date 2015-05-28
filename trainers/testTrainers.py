'''
Test Case 1
Type: Public Hearing
Department: Design and construction
Date Published: April 2, 2015
'''
import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
import os.path
import unittest
import codecs

import adyparser as parser


class PublicHearing(unittest.TestCase):

    # @SkipTest
    def testDesignAndConstruction(self):
        result_fn = os.path.join(os.path.dirname(__file__), 'ad-result1.txt')
        expected = open(result_fn).readlines()
        expected = [e.strip() for e in expected]

        trainer_fn = os.path.join(os.path.dirname(__file__), 'ad-trainer1.txt')
        text = codecs.open(trainer_fn, 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        print addresses
        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)

        # check to see if everything was found
        self.assertEqual(expected, [])


    # @SkipTest
    def testDepartmentOfConsumerAffairs(self):
        result_fn = os.path.join(os.path.dirname(__file__), 'ad-result2.txt')
        expected = open(result_fn).readlines()
        expected = [e.strip() for e in expected]

        trainer_fn = os.path.join(os.path.dirname(__file__), 'ad-trainer2.txt')
        text = codecs.open(trainer_fn, 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)

        # check to see if everything was found
        self.assertEqual(expected, [])


    # @SkipTest
    def testDepartmentOfTransportation(self):
        result_fn = os.path.join(os.path.dirname(__file__), 'ad-result3.txt')
        expected = open(result_fn).readlines()
        expected = [e.strip() for e in expected]

        trainer_fn = os.path.join(os.path.dirname(__file__), 'ad-trainer3.txt')
        text = codecs.open(trainer_fn, 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        print expected
        print 'addresses = ', addresses
        for loc in addresses:
            print 'found: ', loc
            self.assertIn(loc, expected)
            expected.remove(loc)

        # check to see if everything was found
        self.assertEqual(expected, [])

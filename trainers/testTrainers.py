'''
Test Case 1
Type: Public Hearing
Department: Design and construction
Date Published: April 2, 2015
'''
import sys
sys.path.append('..')

import os.path
import unittest
import codecs

import adyparser as parser


class Trainers(unittest.TestCase):

    def testPublicHearings(self):
        result_fn = os.path.join(os.path.dirname(__file__), 'ad-result1.txt')
        expected = open(result_fn).readlines()
        # expected = open('ad-result1.txt').readlines()
        expected = [e.strip() for e in expected]

        trainer_fn = os.path.join(os.path.dirname(__file__), 'ad-result1.txt')
        text = codecs.open(trainer_fn, 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        for loc in addresses:
            self.assertIn(loc, expected)

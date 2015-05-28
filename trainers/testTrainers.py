'''
Test Case 1
Type: Public Hearing
Department: Design and construction
Date Published: April 2, 2015
'''
import sys
sys.path.append('..')

import unittest
import codecs

import adyparser as parser


class Trainers(unittest.TestCase):

    def testPublicHearings(self):
        expected = open('ad-result1.txt').readlines()
        expected = [e.strip() for e in expected]

        text = codecs.open('ad-trainer1.txt', 'r', encoding='utf8').read()
        addresses = parser.parse(text)
        for loc in addresses:
            self.assertIn(loc, expected)

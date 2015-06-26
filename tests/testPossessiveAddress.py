import sys
sys.path.append('..')

# from nose.plugins.skip import SkipTest
# from nose.plugins.attrib import attr

import unittest
from nyctext import nycaddress as parser


class PosessoveAddress(unittest.TestCase):

    def testSaintAnneAvenue(self):
        'Name with apostrophe'
        expected = [u"600 Saint Ann's Avenue Bronx, NY"]
        text = "Academy of Science: 600 Saint Ann's Avenue Bronx, NY"
        address = parser.parse(text)[0]
        self.assertIn(address, expected)

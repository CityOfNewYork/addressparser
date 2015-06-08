# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
import os.path
import unittest
import codecs
import util

import nycaddress as parser


class UnitFilters(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(UnitFilters, self).__init__(*args, **kwds)
        self.cwd = os.path.dirname(__file__)

    def checkExpectation(self, text, expect):
        self.assertEqual(text, expect)


    def testFilterBoroughs(self):
        "handle 'in the borough of (...)' mappings"

        boroughs = 'Brooklyn, Bronx, Queens, Staten Island, Manhattan'.split(', ')
        src = '123 Burro St. in the borough of %s'
        exp = '123 Burro St. %s, NY.\n'

        tests = [dict(text=src%b, expect=exp%b) for b in boroughs]

        for d in tests:
            self.checkExpectation(util.filter_boroughs(d['text']), d['expect'])


    def testFilterBlockCodes(self):
        "handle blockcodes"

        blockcodes = [
            "BOROUGH OF QUEENS 15-5446-Block 1289, lot 15–",
            "BOROUGH OF BROOKLYN 15-7494-Block 2382, lot 3–",
            "BOROUGH OF MANHATTAN 15-6223 – Block 15, lot 22-"]

        for bc in blockcodes:
            print bc
            text = 'A '+ bc + '123 Burrito Boulevard, Brooklyn NY'
            text = text.replace('\x80','').replace('\x93', '')
            # text = text.replace(u'\xa0','')
            # text = text.decode('unicode_escape').encode('ascii','ignore')
            print text
            text = util.filter_blockcodes(text)
            exp = 'A .\n123 Burrito Boulevard, Brooklyn NY'
            self.checkExpectation(text, exp)

    @SkipTest
    def filterStreetAbbreviations(self):
        pass




# -*- coding: utf-8 -*-
from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectations


class UnitFilters(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(UnitFilters, self).__init__(*args, **kwds)

    def testFilterBoroughs(self):
        "handle 'in the borough of (...)' mappings"

        boroughs = 'Brooklyn, Bronx, Queens, Staten Island, Manhattan' \
            .split(', ')
        src = '123 Burro St. in the borough of %s'
        exp = '123 Burro Street %s, NY'

        source, expected = [], []

        for b in boroughs:
            source.append(src % b)
            expected.append(exp % b)

        source = '.\n'.join(source)
        self.checkExpectation(source, expected)

    def testFilterBlockCodes(self):
        "handle blockcodes"

        blockcodes = [
            "BOROUGH OF QUEENS 15-5446-Block 1289, lot 15-",
            "BOROUGH OF BROOKLYN 15-7494-Block 2382, lot 3-",
            "BOROUGH OF MANHATTAN 15-6223 - Block 15, lot 22-"
        ]
        blockcodes = [b.replace('\x80', '').replace('\x93', '')
                      for b in blockcodes]

        source, expected = [], []
        for bc in blockcodes:
            source.append('A ' + bc + '123 Burrito Boulevard, Brooklyn NY')
            expected.append('123 Burrito Boulevard, Brooklyn NY')

        source = '.\n'.join(source)
        self.checkExpectation(source, expected)

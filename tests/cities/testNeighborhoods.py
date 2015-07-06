# -*- coding: utf-8 -*-
from nose.plugins.skip import SkipTest
import pytest
from ..expectations import ParseExpectations


class Neighborhoods(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(Neighborhoods, self).__init__(*args, **kwds)

    def testHistoricNeighborhoods(self):
        'parse historic marked queens neighborhoods'

        text = u'''CERTIFICATE OF APPROPRIATENESS
        BOROUGH OF QUEENS 14-8118-Block 8041, lot 47-
        121 Arleigh Road-Douglaston Historic District'''

        expected = '121 Arleigh Road, Douglaston, Queens, NY'
        expected = [expected]
        self.checkExpectation(text, expected)

    def testNoSubsInWord(self):
        'Neighborhood substitution should be on word boundaries'
        text = "4902 FORT HAMILTON PARKWAY BROOKLYN, NY"
        expected = "4902 FORT HAMILTON PARKWAY BROOKLYN, NY"
        expected = [expected]
        self.checkExpectation(text, expected)

    def testNoMappingOnPostConditions(self):
        'Neighborhood + |N|S|W|E|NORTH|SOUTH|EAST|WEST ok'

        directions = 'North South East West N S E W'.split(' ')
        expand = {'N': 'North', 'S': 'South', 'E': 'East', 'W': 'West'}
        source = []
        expected = []
        for d in directions:
            source.append("19 Union Square %s , New York, NY" % d)
            expected.append("19 Union Square %s, Manhattan, NY"
                            % expand.get(d, d))

        source = '.\n'.join(source)
        self.checkExpectation(source, expected)

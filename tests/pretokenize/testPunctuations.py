from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectations


class PunctuationManipulation(ParseExpectations):
    '''Add description HERE
    '''

    def __init__(self, *args, **kwds):
        super(PunctuationManipulation, self).__init__(*args, **kwds)

    def testPeriodBetweenNNPAndThroughfare(self):
        'wipe out the following period: NNP . LU'


        names = [
            'avenue', 'boulevard',
            'broadway', 'circle', 'crescent',
            'drive', 'expressway', 'highway',
            'lane', 'park', 'piers',
            'place', 'plaza', 'road',
            'slip', 'square', 'street',
            'terrace', 'turnpike'
        ]
        for name in names:
            source = "65 Greene. %s 4th Floor, New York, NY" % name
            expected = "65 Greene %s 4th Floor, Manhattan, NY" % name
            expected = [expected]

            self.checkExpectation(source, expected)

    def testPeriodAfterThroughfareName(self):
        'wipe out period after throughfare name'

        source = "BlackFeet Films: 132 Lexington Avenue. , Brooklyn, NY"
        expected = "132 Lexington Avenue, Brooklyn, NY"
        expected = [expected]
        self.checkExpectation(source, expected)


    def testDoubleCommas(self):
        'remove double commas to single occurence'

        source = "10  8TH AVENUE  BROOKLYN,, NY"
        expected = "10 8TH AVENUE BROOKLYN, NY"
        expected = [expected]
        self.checkExpectation(source, expected)

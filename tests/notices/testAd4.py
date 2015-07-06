from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectationsFromFile


class LandmarkPreservation(ParseExpectationsFromFile):

    def __init__(self, *args, **kwds):
        super(LandmarkPreservation, self).__init__(*args, **kwds)

    @attr(test='wip')
    def testLandmarkPreservation(self):
        'landmark preservation sample'
        self.checkExpectation('ad-sample4.txt', 'ad-expected4.txt')

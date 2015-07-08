import pytest
from ..expectations import ParseExpectationsFromFile


class LandmarkPreservation(ParseExpectationsFromFile):

    def __init__(self, *args, **kwds):
        super(LandmarkPreservation, self).__init__(*args, **kwds)

    def testLandmarkPreservation(self):
        'landmark preservation sample'
        self.checkExpectation('ad-sample4.txt', 'ad-expected4.txt')

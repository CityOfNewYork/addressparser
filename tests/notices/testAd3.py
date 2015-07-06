from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectationsFromFile


class DepartmentOfTransportation(ParseExpectationsFromFile):

    def __init__(self, *args, **kwds):
        super(DepartmentOfTransportation, self).__init__(*args, **kwds)

    def testDepartmentOfTransportation(self):
        'department of transportation sample'
        self.checkExpectation('ad-sample3.txt', 'ad-expected3.txt')

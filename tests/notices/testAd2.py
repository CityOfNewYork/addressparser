from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectations


class DepartmentOfConsumerAffairs(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(DepartmentOfConsumerAffairs, self).__init__(*args, **kwds)

    def testDepartmentOfConsumerAffairs(self):
        'department of consumer affairs sample'
        self.checkExpectation('ad-sample2.txt', 'ad-expected2.txt')

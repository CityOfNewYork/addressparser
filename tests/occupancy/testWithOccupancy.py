from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr

from ..expectations import ParseExpectations


class WithOccupancy(ParseExpectations):
    '''Addresses with Occupancy tags
    '''

    def __init__(self, *args, **kwds):
        super(WithOccupancy, self).__init__(*args, **kwds)

    def testHandleFloor_flr_period(self):
        'process addresses with floor (flr.)'

        source = "DoSomething.org: 19 West 21st St, 8th Flr. , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_flr(self):
        'process addresses with floor (flr)'

        source = "DoSomething.org: 19 West 21st St, 8th Flr, New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_fl_period(self):
        'process addresses with floor (flr.)'

        source = "DoSomething.org: 19 West 21st St, 8th Fl. , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testHandleFloor_fl(self):
        'process addresses with floor (flr)'

        source = "DoSomething.org: 19 West 21st St, 8th Fl , New York, NY"
        expected = "19 West 21st Street 8th Floor Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

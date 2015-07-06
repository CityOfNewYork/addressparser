from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectations
import pytest


@pytest.mark.abbr
class CityAbbreviations(ParseExpectations):
    '''Expand city abbreviations
    '''

    def __init__(self, *args, **kwds):
        super(CityAbbreviations, self).__init__(*args, **kwds)

    def testManhttan(self):
        'test manhttan'

        source = "CHARLES B. MANUELJR: 237  PARK AVENUE  MANHTTAN, NY"
        expected = "237 PARK AVENUE Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testNewYorkCity(self):
        'test New York City'

        source = "CHARLES B. MANUELJR: 237  PARK AVENUE  New York City, NY"
        expected = "237 PARK AVENUE Manhattan, NY"
        expected = [expected]

        self.checkExpectation(source, expected)

    def testBrooklynExpands(self):
        'various brooklyn abbreviations expand'
        source = """
            9002  FIFTH AVE  BKYLN, NY.
            100  WOODRUFF AVE  BROOLKYN, NY.
            105  WOODRUFF AVE  BROOKYLN, NY.
            258  UNION ST  BK, NY.
            155 THIRD STREET BRROKLYN, NY.
        """
        expected = [
            "9002 FIFTH Avenue Brooklyn, NY",
            "100 WOODRUFF Avenue Brooklyn, NY",
            "105 WOODRUFF Avenue Brooklyn, NY",
            "258 UNION Street Brooklyn, NY",
            "155 THIRD STREET Brooklyn, NY",
        ]

        self.checkExpectation(source, expected)

    def testBronxExpands(self):
        'various bronx abbreviations expand'
        source = "12  WEST BURNSIDE AVE  BX, NY"
        expected = "12 WEST BURNSIDE Avenue Bronx, NY"
        expected = [expected]
        self.checkExpectation(source, expected)

    def testNYNYExpands(self):
        'ny ny expands'

        source = """
            9000  FIFTH AVE  NY, NY.
            9001  FIFTH AVE  NY, New York.
            9002  FIFTH AVE  New York, NY.
            9003  FIFTH AVE  New York, New York.
            10 E 40TH Street NYC, NY
        """
        expected = [
            "9000 FIFTH Avenue Manhattan, NY",
            "9001 FIFTH Avenue Manhattan, NY",
            "9002 FIFTH Avenue Manhattan, NY",
            "9003 FIFTH Avenue Manhattan, NY",
            "10 E 40TH Street Manhattan, NY",
        ]
        self.checkExpectation(source, expected)

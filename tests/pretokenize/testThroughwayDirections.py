from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ..expectations import ParseExpectations


class ThroughwayTests(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(ThroughwayTests, self).__init__(*args, **kwds)

    def testSouths(self):
        'various southern directions recognized'

        source = """
            404  PARK AVE. S. NEW YORK, NY.
            405  PARK AVE. SO. NEW YORK, NY.
            406  PARK AVE. SOUTH. NEW YORK, NY.
            409  PARK AVE. SOUTH NEW YORK, NY.
        """

        expected = [
            "404 PARK Avenue South, Manhattan, NY",
            "405 PARK Avenue South, Manhattan, NY",
            "406 PARK Avenue South, Manhattan, NY",
            "409 PARK Avenue South, Manhattan, NY"
        ]
        self.checkExpectation(source, expected, True)

    def testNorths(self):
        'various northern directions recognized'

        source = """
            404  PARK AVE. N. NEW YORK, NY.
            405  PARK AVE. NO. NEW YORK, NY.
            406  PARK AVE. NORTH. NEW YORK, NY.
            409  PARK AVE. NORTH NEW YORK, NY.
        """

        expected = [
            "404 PARK Avenue North, Manhattan, NY",
            "405 PARK Avenue North, Manhattan, NY",
            "406 PARK Avenue North, Manhattan, NY",
            "409 PARK Avenue North, Manhattan, NY"
        ]
        self.checkExpectation(source, expected, True)

    def testEasts(self):
        'various Eastern directions recognized'

        source = """
            404  PARK AVE. E. NEW YORK, NY.
            405  PARK AVE. EAST. NEW YORK, NY.
            406  PARK AVE. EAST NEW YORK, NY.
        """

        expected = [
            "404 PARK Avenue East, Manhattan, NY",
            "405 PARK Avenue East, Manhattan, NY",
            "406 PARK Avenue East, Manhattan, NY",
        ]
        self.checkExpectation(source, expected)

    def testWests(self):
        'various Eastern directions recognized'

        source = """
            404  PARK AVE. W. NEW YORK, NY.
            405  PARK AVE. WEST. NEW YORK, NY.
            406  PARK AVE. WEST NEW YORK, NY.
        """

        expected = [
            "404 PARK Avenue West, Manhattan, NY",
            "405 PARK Avenue West, Manhattan, NY",
            "406 PARK Avenue West, Manhattan, NY",
        ]
        self.checkExpectation(source, expected)

    def testStreetNames(self):
        'concourse and loop recognized'
        source = """
            590 GRAND CONCOURSE BRONX, NY.
            149 DREISER LOOP BRONX, NY.
        """
        expected = [
            "590 GRAND CONCOURSE BRONX, NY",
            "149 DREISER LOOP BRONX, NY"
        ]
        self.checkExpectation(source, expected)

    def testSquareAbbreviation(self):
        'sq expands to square'
        source = """
            41 Union Sq. West suite 1024, New York, NY.
            51 Union Sq West suite 10, New York, NY.
        """
        expected = [
            "41 Union Square West, suite 1024, Manhattan, NY",
            "51 Union Square West, suite 10, Manhattan, NY"
        ]
        self.checkExpectation(source, expected)


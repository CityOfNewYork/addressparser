import pytest
from ..expectations import ParseExpectations


class SplitNumberFromDirections(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(SplitNumberFromDirections, self).__init__(*args, **kwds)

    def test_separation(self):
        'separate number from direction'

        source = """
            14EAST 28TH STREET SUITE 335 NEWYORK, NY.
            15EAST. 28TH STREET SUITE 335 NEWYORK, NY.
            16E 28TH STREET SUITE 335 NEWYORK, NY.
            17E. 28TH STREET SUITE 335 NEWYORK, NY.
        """
        expected = [
            "14 EAST 28TH STREET SUITE 335 Manhattan, NY",
            "15 EAST 28TH STREET SUITE 335 Manhattan, NY",
            "16 E 28TH STREET SUITE 335 Manhattan, NY",
            "17 E 28TH STREET SUITE 335 Manhattan, NY",
        ]

        self.checkExpectation(source, expected)

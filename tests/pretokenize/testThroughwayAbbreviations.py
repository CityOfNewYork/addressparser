import pytest
from ..expectations import ParseExpectations


@pytest.mark.wip
class ThroughwayAbbreviations(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(ThroughwayAbbreviations, self).__init__(*args, **kwds)

    def test_two_and_three_ltr_abbreviations(self):
        count = 22
        abbrs = 'av ave blv blvd pkw pkwy pl plz st str'.split(' ')
        lookup = {"av": "Avenue", "bl": "Boulevard", "pk": "Parkway",
                  "pl": "Plaza", "st": "Street"}
        source = []
        expected = []
        tmp1 = '%d Acacia %s Queens, NY'
        tmp2 = '%d Acacia %s. Queens, NY'
        exp = '%d Acacia %s Queens, NY'

        for ab in abbrs:
            source.append(tmp1 % (count, ab))
            expected.append(exp % (count, lookup[ab[:2]]))
            count += 1
            source.append(tmp2 % (count, ab))
            expected.append(exp % (count, lookup[ab[:2]]))
            count += 1

        source = '.\n'.join(source)
        self.checkExpectation(source, expected, True)

    def test_fixed_ltr_abbreviations(self):
        count = 22
        abbrs = 'cir dr expy hwy ln pk rd sq'.split(' ')
        lookup = {"ci": "Circle", "dr": "Drive", "ex": "Expressway",
                  "hw": "Highway", "ln": "Lane", "pk": "Park",
                  "rd": "Road", "sq": "Square"}
        source = []
        expected = []
        tmp1 = '%d Acacia %s Queens, NY'
        tmp2 = '%d Acacia %s. Queens, NY'
        exp = '%d Acacia %s Queens, NY'

        for ab in abbrs:
            source.append(tmp1 % (count, ab))
            expected.append(exp % (count, lookup[ab[:2]]))
            count += 1
            source.append(tmp2 % (count, ab))
            expected.append(exp % (count, lookup[ab[:2]]))
            count += 1

        source = '.\n'.join(source)
        self.checkExpectation(source, expected, True)

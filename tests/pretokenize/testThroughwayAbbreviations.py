import pytest
from ..expectations import ParseExpectations


@pytest.mark.wip
class ThroughwayAbbreviations(ParseExpectations):

    def __init__(self, *args, **kwds):
        super(ThroughwayAbbreviations, self).__init__(*args, **kwds)

    def test_abbreviations(self):
        count = 22
        abbrs = 'av ave blv blvd pkw pkwy pl plz st str ' \
                'cir dr expy hwy ln pk rd sq'.split(' ')
        lookup = {
            "av": "Avenue",
            "bl": "Boulevard",
            "ci": "Circle",
            "dr": "Drive",
            "ex": "Expressway",
            "hw": "Highway",
            "ln": "Lane",
            "pk": "Park",
            "pkw": "Parkway",  # only 3 character key
            "pl": "Plaza",
            "rd": "Road",
            "sq": "Square",
            "st": "Street",
        }
        source = []
        expected = []
        tmp1 = '%d Acacia %s Queens, NY'
        tmp2 = '%d Acacia %s. Queens, NY'
        exp = '%d Acacia %s Queens, NY'

        for ab in abbrs:
            expansion = lookup[ab[:2]]
            if ab.startswith('pkw'):
                expansion = lookup['pkw']

            source.append(tmp1 % (count, ab))
            expected.append(exp % (count, expansion))
            count += 1
            source.append(tmp2 % (count, ab))
            expected.append(exp % (count, expansion))
            count += 1

        source = '.\n'.join(source)
        self.checkExpectation(source, expected, True)

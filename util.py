import re

_rex_boroughs = re.compile('(in\s+the\s+)Borough\s+of\s+'
                           '(Brooklyn|Queens|Staten\s+Island|Bronx)',
                           re.IGNORECASE)

_rex_manhattan = re.compile('(in\s+the\s+)Borough\s+of\s+'
                            '(Manhattan)',
                            re.IGNORECASE)


def filter_boroughs(text):
    global _rex_boroughs, _rex_manhattan
    text = _rex_manhattan.sub('NY, NY', text)
    return _rex_boroughs.sub('\\2, NY', text)


def preproces_text(text):
    return filter_boroughs(text)


def location_to_string(tree):
    return ' '.join([c[0] for c in tree])


def showResults(res):
    for ad in res:
        print location_to_string(ad)


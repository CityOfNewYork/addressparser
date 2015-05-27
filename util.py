import re

_rex = re.compile('Borough\s+of\s+'
                  '(Manhattan|Brooklyn|Queens|Staten\s+Island|Bronx)',
                  re.IGNORECASE)


def filter_boroughs(text):
    global _rex
    text = text.replace('in the Borough of Manhattan', 'NY, NY') \
        .replace('in the Borough of Brooklyn', 'Brooklyn, NY') \
        .replace('in the Borough of Queens', 'Queens, NY') \
        .replace('in the Borough of Staten Island', 'SI, NY') \
        .replace('in the Borough of Bronx', 'BX, NY')
    return _rex.sub('\\1, Ny', text)


def preproces_text(text):
    return filter_boroughs(text)


def location_to_string(tree):
    return ' '.join([c[0] for c in tree])


def showResults(res):
    for ad in res:
        print location_to_string(ad)


import re
from throughways import names as throughway_names


def make_neighorbood_regex(lHoods, city):

    hoods = '|'.join(lHoods)

    # Don't match if neighborhood is followed
    # by a thoroughfare name
    names = throughway_names[1:-1]  # remove parens
    names = '(%s|%s|north|south|east|west|n[\s\.,]|s[\s\.,]|w[\s\.,]|e[\s\.,])' % (names, city)

    rex = '\\s((%s)(\\s|,))(?!([\\s|,]*(%s)))' % (hoods, names)
    return re.compile(rex, re.I)

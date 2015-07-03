import re
'''Process to be done before tokenizing into sentences.
Transorm the text so the sentence tokenizer can break
sentences correctly.

Another alternative is to examine a wrapper for
sent_tokenize that could stitch sentence fragments
together.

'''
_rex_initials = re.compile('(?<=[\s\.][A-Z])(\.)', re.I)

_rex_reverend = re.compile('rev\.', re.I)
_rex_suite = re.compile('ste\.', re.I)

_street_abbreviations = re.compile('\s+(str?\.?)[\s,]', re.IGNORECASE)
_avenue_abbreviations = re.compile('\s+(ave?\.?)[\s,]', re.IGNORECASE)
_boulevard_abbreviations = re.compile('\s+(blvd?\.?)[\s,]', re.IGNORECASE)
_plaza_abbreviations = re.compile('\s+(plz?\.?)[\s,]', re.IGNORECASE)
_drive_abbreviations = re.compile('\s+(dr?\.?)[\s,]', re.IGNORECASE)
_parkway_abbreviations = re.compile('\s+(pkwy?\.?)[\s,]', re.IGNORECASE)
_road_abbreviations = re.compile('\s+(rd\.?)[\s,]', re.IGNORECASE)
_lane_abbreviations = re.compile('\s+(ln\.?)[\s,]', re.IGNORECASE)
_expressway_abbreviations = re.compile('\s+(expy\.?)[\s,]', re.IGNORECASE)
_highway_abbreviations = re.compile('\s+(hwy\.?)[\s,]', re.IGNORECASE)
_circle_abbreviations = re.compile('\s+(cir\.?)[\s,]', re.IGNORECASE)


def do_street_abbreviations(text):
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html

    global _street_abbreviations, _avenue_abbreviations
    global _boulevard_abbreviations, _plaza_abbreviations, _drive_abbreviations
    global _parkway_abbreviations, _road_abbreviations, _lane_abbreviations

    text = _street_abbreviations.sub(' Street ', text)
    text = _avenue_abbreviations.sub(' Avenue ', text)
    text = _boulevard_abbreviations.sub(' Boulevard ', text)
    text = _plaza_abbreviations.sub(' Plaza ', text)
    text = _drive_abbreviations.sub(' Drive ', text)
    text = _parkway_abbreviations.sub(' Parkway ', text)
    text = _road_abbreviations.sub(' Road ', text)
    text = _lane_abbreviations.sub(' Lane ', text)
    text = _expressway_abbreviations.sub(' Expressway ', text)
    text = _highway_abbreviations.sub(' Highway ', text)
    text = _circle_abbreviations.sub(' Circle ', text)
    return text


_rex_cd = re.compile(r'\s?(\d+)(n|s|e|w)(\.)?\s', re.I)

# 110E 21st -> 100 E 21 st
# 110E 22nd
# 110E 23rd
# 110E 24th
# 110E 25th.


def do_cd(text):
    global _rex_cd
    return _rex_cd.sub('\\1 \\2 ', text)


def do_initials(text):
    global _rex_initials
    return _rex_initials.sub(' ', text)


def do_title(text):
    global _rex_reverend
    return _rex_reverend.sub('Rev', text)


def do_suite(text):
    global _rex_suite
    return _rex_suite.sub('Suite', text)

_rex_periods = re.compile('(?<=[^\s])(\.)(?=\s)', re.I)


def do_periods(text):
    global _rex_periods
    return _rex_periods.sub(' ', text)


_rex_ordinal_indicator_st = re.compile('(\d+)(?<!1)(st\.?)', re.I)
_rex_ordinal_indicator_rd = re.compile('(\d+)(?<!3)(rd\.?)', re.I)


def do_ordinal_indicator(text):
    '''Removes bad ordinal indicators that could be
    road(rd) or street(st)
    Transform yes:    22st -> 22 st
    Transform  no:    21st -> 21st

    '''
    global _ordinal_indicator_st, _ordinal_indicator_rd

    text = _rex_ordinal_indicator_st.sub('\\1 \\2', text)
    text = _rex_ordinal_indicator_rd.sub('\\1 \\2', text)
    return text


def transform(text, verbose=False):
    if verbose:
        print 'Source Text: %s' % text

    text = do_periods(text)
    if verbose:
        print '    Periods: %s' % text

    text = do_initials(text)
    if verbose:
        print '   Initials: %s' % text

    text = do_title(text)
    if verbose:
        print '   titlesub: %s' % text

    text = do_suite(text)
    if verbose:
        print '   suitesub: %s' % text

    text = do_ordinal_indicator(text)
    if verbose:
        print 'ordinal indicator: %s' % text

    text = do_street_abbreviations(text)
    if verbose:
        print 'street abbr: %s' % text

    text = do_cd(text)
    if verbose:
        print '    cd abbr: %s' % text

    return text

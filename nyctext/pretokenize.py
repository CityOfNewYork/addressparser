import re
'''Process to be done before tokenizing into sentences.
Transorm the text so the sentence tokenizer can break
sentences correctly.

Another alternative is to examine a wrapper for
sent_tokenize that could stitch sentence fragments
together.

'''

_street_abbreviations = re.compile('\s+(str?\.?)[\s,]', re.IGNORECASE)
_avenue_abbreviations = re.compile('\s+(ave?\.?)[\s,]', re.IGNORECASE)
_boulevard_abbreviations = re.compile('\s+(blvd?\.?)[\s,]', re.IGNORECASE)
_plaza_abbreviations = re.compile('\s+(plz?\.?)[\s,]', re.IGNORECASE)
_drive_abbreviations = re.compile('\s+(dr?\.?)[\s,]', re.IGNORECASE)
_parkway_abbreviations = re.compile('\s+(pkwy?\.?)[\s,]', re.IGNORECASE)
_road_abbreviations = re.compile('\s+(rd\.?)[\s,]', re.IGNORECASE)


def filter_street_abbreviations(text):
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html

    global _street_abbreviations, _avenue_abbreviations
    text = _street_abbreviations.sub(' Street ', text)
    text = _avenue_abbreviations.sub(' Avenue ', text)
    text = _boulevard_abbreviations.sub(' Boulevard ', text)
    text = _plaza_abbreviations.sub(' Plaza ', text)
    text = _drive_abbreviations.sub(' Drive ', text)
    text = _parkway_abbreviations.sub(' Parkway ', text)
    text = _road_abbreviations.sub(' Road ', text)
    return text


def do_cd(text):
    _rex_cd = re.compile(r'\s?(\d+)(n|s|e|w)(\.)?\s', re.I)
    return _rex_cd.sub('\\1 \\2 ', text)


def do_initials(text):
    _rex_initials = re.compile('(?<=[\s\.][A-Z])(\.)', re.I)
    return _rex_initials.sub(' ', text)


def do_title(text):
    _rex_reverend = re.compile('rev\.', re.I)
    return _rex_reverend.sub('Rev', text)


def do_suite(text):
    _rex_suite = re.compile('ste\.', re.I)
    return _rex_suite.sub('Suite', text)


def do_periods(text):
    _rex_periods = re.compile('(?<=[^\s\s])(\.)(?=\s)', re.I)
    return _rex_periods.sub('\\1 ', text)


def do_ordinal_indicator(text):
    '''Removes bad ordinal indicators that could be
    road(rd) or street(st)
    Transform yes:    22st -> 22 st
    Transform  no:    21st. -> 21st

    '''
    _rex_bad_ord_indic_st = re.compile('(\d+)(?<!1)(st\.?)', re.I)
    _rex_bad_ord_indic_rd = re.compile('(\d+)(?<!3)(rd\.?)', re.I)
    _rex_good_ord_indic_st = re.compile('(\d+)(?<=1)(st\.)', re.I)
    _rex_good_ord_indic_rd = re.compile('(\d+)(?<=3)(rd\.)', re.I)

    text = _rex_bad_ord_indic_st.sub('\\1 st', text)
    text = _rex_bad_ord_indic_rd.sub('\\1 rd', text)

    text = _rex_good_ord_indic_st.sub('\\1st', text)
    text = _rex_good_ord_indic_rd.sub('\\1rd', text)
    return text


def do_city_abbreviations(text):
    abr_brooklyn = re.compile('\s[\s,]*((bklyn|bkln)[\s,]*)', re.I)
    abr_manhattan = re.compile('\s[\s,]*((manhttan|new york city)[\s,]*)', re.I)

    text = abr_brooklyn.sub(' Brooklyn ', text)
    text = abr_manhattan.sub(' Manhattan, ', text)

    return text


def do_occupancy_abbreviations(text):
    rex_floor = re.compile('([\s,]flr?\.?[\s\.]*)[\s,]', re.I)
    text = rex_floor.sub(' Floor ', text)
    return text


def transform(text, verbose=False):
    if verbose:
        print 'Source Text: %s' % text

    text = filter_street_abbreviations(text)
    if verbose:
        print 'street Abbr: %s' % text

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
        print '  ord indic: %s' % text

    text = do_occupancy_abbreviations(text)
    if verbose:
        print 'occu abbrev: %s' % text

    text = do_city_abbreviations(text)
    if verbose:
        print '  city abbr: %s' % text

    text = do_cd(text)
    if verbose:
        print '    cd abbr: %s' % text

    return text

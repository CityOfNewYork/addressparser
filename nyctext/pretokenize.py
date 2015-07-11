# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

import re
'''Process to be done before tokenizing into sentences.
Transorm the text so the sentence tokenizer can break
sentences correctly.

Another alternative is to examine a wrapper for
sent_tokenize that could stitch sentence fragments
together.

'''
import nltk
from nltk.tokenize import word_tokenize
from tagger import transform_tags
from neighborhoods import throughway_names


def do_periods(text):
    '''Replace all surrounded periods with a period-space
    '''
    rex = re.compile(r'(\b\.\b)', re.I)
    return rex.sub('\\1 ', text)


def remove_commas_multiple_occurences(text):
    rex = re.compile('(\s*\,[\,\s]*)', re.I)
    return rex.sub(', ', text)


def remove_period_after_throughway_name(text):
    rex = re.compile('%s\s*(\.\s+)' % throughway_names, re.I)
    return rex.sub('\\1 ', text)


def remove_period_between_nnp_and_lu(text):

    tokens = word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    tags = transform_tags(tags, text)

    # no periods between NNP and LU
    _text = [tags[0][0]]
    for dx in range(1, len(tags)-1):
        prevTag = tags[dx-1][1]
        val, tag = tags[dx]
        if val == '.' and prevTag == 'NNP' and tags[dx+1][1] == 'LU':
            continue
        _text.append(val)
    _text.append(tags[-1][0])

    # remove spaces
    savespace = re.compile('\s+([,\.])', re.I)
    return savespace.sub('\\1 ', ' '.join(_text))


def filter_street_abbreviations(text):
    # Todo: Build a more comprehensive list of throughways.
    # See: http://www.semaphorecorp.com/cgi/abbrev.html
    _avenue_abbreviations = re.compile('\s+(ave?\.?)[\s,]', re.I)
    _boulevard_abbreviations = re.compile('\s+(blvd?\.?)[\s,]', re.I)
    _circle_abbreviations = re.compile('\s+(cir\.?)[\s,]', re.I)
    _drive_abbreviations = re.compile('\s+(dr\.?)[\s,]', re.I)
    _expressway_abbreviations = re.compile('\s+(expy\.?)[\s,]', re.I)
    _highway_abbreviations = re.compile('\s+(hwy\.?)[\s,]', re.I)
    _lane_abbreviations = re.compile('\s+(ln\.?)[\s,]', re.I)
    _park_abbreviations = re.compile('\s+(pk?\.?)[\s,]', re.I)
    _parkway_abbreviations = re.compile('\s+(pkwy?\.?)[\s,]', re.I)
    _plaza_abbreviations = re.compile('\s+(plz?\.?)[\s,]', re.I)
    _road_abbreviations = re.compile('\s+(rd\.?)[\s,]', re.I)
    _square_abbreviations = re.compile('\s+(sq\.?)[\s,]', re.I)
    _street_abbreviations = re.compile('\s+(str?\.?)[\s,]', re.I)


    text = _avenue_abbreviations.sub(' Avenue ', text)
    text = _boulevard_abbreviations.sub(' Boulevard ', text)
    text = _circle_abbreviations.sub(' Circle ', text)
    text = _drive_abbreviations.sub(' Drive ', text)
    text = _expressway_abbreviations.sub(' Expressway ', text)
    text = _highway_abbreviations.sub(' Highway ', text)
    text = _lane_abbreviations.sub(' Lane ', text)
    text = _park_abbreviations.sub(' Park ', text)
    text = _parkway_abbreviations.sub(' Parkway ', text)
    text = _plaza_abbreviations.sub(' Plaza ', text)
    text = _road_abbreviations.sub(' Road ', text)
    text = _square_abbreviations.sub(' Square ', text)
    text = _street_abbreviations.sub(' Street ', text)
    return text


def expand_street_post_directions(text):
    rex_s = "%s[\\s]*([\\,\\s]+(so?|south)[\\s\\,\\.]+)"
    rex_s = rex_s % throughway_names
    rex_s = re.compile(rex_s, re.I)
    text = rex_s.sub('\\1 South, ', text)

    rex_n = "%s[\\s]*([\\,\\s]+(no?|north)[\\s\\,\\.]+)"
    rex_n = rex_n % throughway_names
    rex_n = re.compile(rex_n, re.I)
    text = rex_n.sub('\\1 North, ', text)

    rex_e = "%s[\\s]*([\\,\\s]+(e|east)[\\s\\,\\.]+)"
    rex_e = rex_e % throughway_names
    rex_e = re.compile(rex_e, re.I)
    text = rex_e.sub('\\1 East, ', text)

    rex_w = "%s[\\s]*([\\,\\s]+(w|west)[\\s\\,\\.]+)"
    rex_w = rex_w % throughway_names
    rex_w = re.compile(rex_w, re.I)
    text = rex_w.sub('\\1 West, ', text)

    return text


def do_cd(text):
    _rex_cd = re.compile(r'\b(\d+)(n|s|e|w|north|south|east|west)(\.)?\s', re.I)
    return _rex_cd.sub('\\1 \\2 ', text)


def do_initials(text):
    _rex_initials = re.compile('(?<=[\s\.][A-Z])(\.)', re.I)
    return _rex_initials.sub(' ', text)


def do_title(text):
    _rex_reverend = re.compile('rev\.', re.I)
    return _rex_reverend.sub('Rev', text)


def do_suite(text):
    # _rex_suite = re.compile('ste\.', re.I)
    _rex_suite = re.compile(r'\bste\.', re.I)
    text = _rex_suite.sub('Suite ', text)

    _rex_suite = re.compile(r'\bapt\.', re.I)
    text = _rex_suite.sub('Apt ', text)
    return text


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
    abr_bk = '\s[\s,]*((bk[ly]{2,2}n|bkln|bk|broolkyn|brookyln|brroklyn)[\s,]*)'
    abr_bk = re.compile(abr_bk, re.I)

    abr_man = re.compile('\s[\s,]*((manhttan|new york city|nyc)[\s,]*)', re.I)
    abr_bx = re.compile('\s[\s,]*(bx[\s,]*)', re.I)

    text = abr_bk.sub(' Brooklyn, ', text)
    text = abr_man.sub(' Manhattan, ', text)
    text = abr_bx.sub(' Bronx, ', text)

    return text


def do_occupancy_abbreviations(text):
    rex_floor = re.compile('([\s,]flr?\.?[\s\.]*)[\s,]', re.I)
    text = rex_floor.sub(' Floor ', text)
    return text


def transform(text, verbose=False):

    # import ipdb; ipdb.set_trace()
    if verbose:
        print 'Source Text: %s' % text

    text = do_periods(text)
    if verbose:
        print '    Periods: %s' % text

    text = remove_period_between_nnp_and_lu(text)
    if verbose:
        print 'Pre toknize 1: %s' % text

    text = remove_period_after_throughway_name(text)
    if verbose:
        print 'Pre toknize 2: %s' % text

    text = remove_commas_multiple_occurences(text)
    if verbose:
        print '     Commas: %s' % text

    text = filter_street_abbreviations(text)
    if verbose:
        print 'street Abbr: %s' % text

    text = expand_street_post_directions(text)
    if verbose:
        print 'Post   Abbr: %s' % text

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

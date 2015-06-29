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


def do_initials(text):
    global _rex_initials
    return _rex_initials.sub(' ', text)


def do_title(text):
    global _rex_reverend
    return _rex_reverend.sub('Rev', text)


def transform(text, verbose=False):
    if verbose:
        print 'Source Text: %s' % text

    text = do_initials(text)
    if verbose:
        print '   Initials: %s' % text

    text = do_title(text)
    if verbose:
        print '   titlesub: %s' % text

    return text

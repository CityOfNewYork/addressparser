"""Usage: quick_example.py [options] SOURCE

--trace     Trace the parsing states. Useful for debugging.
--geo       Return Geolocation attributes
Options:
    SOURCE  Quoted text to parse. ie, "1 Centre Street, NY NY"
"""
from docopt import docopt
from os import environ
from nyc_geoclient import Geoclient
from nycaddress import parse, lookup_geo, parse_with_geo


def main(g=None):
    # import codecs
    not_parsed, parsed = [], []
    samples = unparsible()
    # samples = [
    # ]
    for sample in samples:
        print '\n\nSample: %s' % sample
        addresses = parse(sample, verbose=True)
        if not addresses:
            not_parsed.append(sample)
            continue
        parsed.append('%s\n\t\t\t%s' % (sample, addresses[0]))
        if g:
            for address in addresses:
                print 'Address: %s' % address
                print lookup_geo(g, address, False)
                print
        print
        print
    print 'Addresses parsed:'
    for ad in parsed:
        print ad
    print '\n\n'

    print 'Addresses not parsed:'
    for ad in not_parsed:
        print ad

if __name__ == '__main__':
    # https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()

    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)

    args = docopt(__doc__, version='0.1.1rc')
    # import ipdb; ipdb.set_trace()
    addresses = []
    if args['--geo']:
        addresses = parse_with_geo(args['SOURCE'], g, args['--trace'])
    else:
        addresses = parse(args['SOURCE'], args['--trace'])

    for ad in addresses:
        print ad

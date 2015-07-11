# -*- coding: utf-8 -*-
"""
Usage:
    adparse --file=<infile> [--trace]
    adparse [--trace] [--geo] <text>

Options:
    -h --help       Show this screen.
    --version       Show version.
    --file=<infile> Input file.
    --trace         Print trace statement
    --geo           Return Geolocation attributes [default: False]
"""

__author__ = "C. Sudama, Matthew Alhonte"
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"

from docopt import docopt
from os import environ
import codecs
from nyc_geoclient import Geoclient
from nycaddress import parse, parse_with_geo


def do_adhoc(text, g, trace=False, geo=False):
    ads = []
    if args['--geo']:
        ads = parse_with_geo(text, g, trace)
    else:
        ads = parse(text, trace)

    for ad in ads:
        print ad


def do_file(fn, g, trace=False, geo=False):
    total, parsed, failed = 0, 0, 0
    ads = []
    for line in codecs.open(fn, encoding='utf-8'):
        line = line.encode('ascii', 'ignore').strip()
        if line == '':
            continue

        total += 1

        if geo:
            ads = parse_with_geo(line, g, trace)
        else:
            ads = parse(line, trace)

        if ads:
            parsed += 1
            print 'ok: [%s]' % line
        else:
            failed += 1

    print 'Summary:\n\t%04d parsed\n\t%04d failed\n\t%04d Total' \
        % (parsed, failed, total)


if __name__ == '__main__':
    # https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()

    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']
    g = Geoclient(appid, appkey)

    # import ipdb; ipdb.set_trace()
    args = docopt(__doc__, version='0.1.1rc')

    ads = []
    if args['--file']:
        ads = do_file(args['--file'], g,
                      trace=args['--trace'], geo=args['--geo'])
    else:
        do_adhoc(args['<text>'], g,
                 trace=args['--trace'], geo=args['--geo'])

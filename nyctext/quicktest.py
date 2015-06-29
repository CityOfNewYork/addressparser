import codecs
from os import environ
from nyc_geoclient import Geoclient
from nycaddress import parse, lookup_geo


def main():

    # https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']

    # samples = [codecs.open('../tests/data/ad-sample1.txt', 'r',
    #                        encoding='utf8').read()]
    #
    # samples = [
    #     'FRATELLIS MARKET PLACE: 0 WARDS ISLAND/2FL MANHATTAN, NY',
    #     'FRESH DELIGHT: 1 RICHMOND TERRACE STATEN ISLAND, NY',
    # ]
    samples = [
        'Metropolitan High School Inc.: 1180 Rev. J.A. Polite Ave. Bronx, NY'
    ]
    g = Geoclient(appid, appkey)
    for sample in samples:
        print '\n\nSample: %s' % sample
        for address in parse(sample, verbose=True):
            print 'Address: %s' % address
            print lookup_geo(g, address, False)
            print
        print
        print

if __name__ == '__main__':
    main()

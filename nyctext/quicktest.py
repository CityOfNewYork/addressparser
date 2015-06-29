from os import environ
from nyc_geoclient import Geoclient
from nycaddress import parse, lookup_geo


def unparsible():
    return '''ANITA TERRACE OWNERS,INC.: ONE PENN PLAZA SUITE 4000  NEW YORK, NY
701 St. Anns Avenue Bronx, NY'''.split('\n')


def main():
    # import codecs

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
    g = Geoclient(appid, appkey)
    not_parsed = []
    samples = unparsible()

    for sample in samples:
        print '\n\nSample: %s' % sample
        addresses = parse(sample, verbose=True)
        if not addresses:
            not_parsed.append(sample)
            continue
        for address in addresses:
            print 'Address: %s' % address
            print lookup_geo(g, address, False)
            print
        print
        print
    print 'Addresses not parsed:'
    for ad in not_parsed:
        print ad

if __name__ == '__main__':
    main()

'''Script to create json payloads for testing with curl.

'''
import codecs
import json

if __name__ == '__main__':
    for i in range(1, 5):
        infile = 'ad-sample%d.txt' % i
        outfile = 'ad-sample%d.json' % i

        text = codecs.open(infile, 'r', encoding='utf8').read()
        data = {'source': text}
        data = json.dumps(data)

        out = codecs.open(outfile, 'w', encoding='utf8')
        out.write(data)
        out.flush()
        out.close()

from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.tokenize import word_tokenize
import nltk
import codecs
import re
text = codecs.open('trainers/ad-trainer2.txt','r', encoding='utf8').read()
text = text.replace('in the Borough of Manhattan', 'NY, NY')
text = text.replace('in the Borough of Brooklyn', 'Brooklyn, NY')
text = text.replace('in the Borough of Queens', 'Queens, NY')
text = text.replace('in the Borough of Staten Island', 'SI, NY')
text = text.replace('in the Borough of Bronx', 'BX, NY')

rex = re.compile('Borough\s+of\s+(Manhattan|Brooklyn|Queens|Staten\s+Island|Bronx)',re.IGNORECASE)
text = rex.sub('\\1, Ny', text)
text = word_tokenize(text)
print ' '.join(text)
def filter_paren(tup):
    if tup[0] == '(':
        return tup[0], '-NONE-'
    return tup
pos =  nltk.pos_tag(text)
pos = [p for p in pos if p[0] != ',']
print(pos)
pos = map(filter_paren, pos)
print (pos)

def parse1(toks):
    grammer = "Location: {<NNP>+<CD><NNP>+<CD>}"
    cp = nltk.RegexpParser(grammer)
    result = cp.parse(toks)
    return [s for s in result.subtrees(lambda t: t.label() == 'Location')]

def parse2(toks):
#     grammer = "Location: {<CD><NNP>+}"
    grammer = "Location: {<CD><NNP>+<JJ>?<NNP>+|<CD><NNP><CD><NNP>+|<CD>+<NNP>+|<CD><NNP>+}"
    cp = nltk.RegexpParser(grammer)
    result = cp.parse(toks)
    return [s for s in result.subtrees(lambda t: t.label() == 'Location')]

def showResults(res):
    for ad in res:
        address = []
        for component in ad:
            address.append(component[0])
        print ' '.join(address)
        if address[-2].lower() == 'ny' or address[-1].lower() == 'ny' :
            print ' '.join(address)
showResults(parse1(pos))
showResults(parse2(pos))

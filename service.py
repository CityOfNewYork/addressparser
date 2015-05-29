from nycaddress import parse
from flask import Flask, request
import json

app = Flask(__name__)


def parseAddresses(text):
    result = {'addresses': parse(text)}
    return '%s\n\n' % json.dumps(result)


@app.route('/')
def root():
    return """Welcome to the NYC Address Parser BetaNYC."""


@app.route('/parseaddresses/', methods=['GET', 'POST'])
def parseaddresses():
    '''POST Payload:
        {"source": "string"}
    '''
    if request.method == 'GET':
        return 'So, instructions would be printed here...'

    data = request.json
    return parseAddresses(data['source'])

if __name__ == '__main__':
    app.run(debug=True)

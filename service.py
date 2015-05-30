from nycaddress import parse
from flask import Flask, request, jsonify
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*', allow_headers='Content-Type')


def parseAddresses(text):
    return jsonify({'addresses':
                    [{"text": loc} for loc in parse(text)]})


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

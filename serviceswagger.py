# -*- coding: utf-8 -*-
from nycaddress import parse
from flask import Flask, request, jsonify
from flask_swagger import swagger

# from flask.ext.cors import CORS
# CORS(app, resources=r'/*', allow_headers='Content-Type')

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         "Authorization, Content-Type")
    response.headers.add('Access-Control-Expose-Headers', "Authorization")
# "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Methods',
                         "GET, POST")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
    return response


def parseAddresses(text):
    return jsonify({'addresses':
                    [{"text": loc} for loc in parse(text)]})


@app.route('/', methods=['GET'])
def index():
    return "BetaNYC 5 Borough's address finder"


@app.route('/api/parseaddresses', methods=['POST'])
def parseaddresses():
    """
    Parse Addresses
    The only endpoint used to submit a string to be parsed.
    ---
    responses:
        '200':
            description: list of addresses.
            schema:
                id: StreetAddress
                required:
                    - text
                properties:
                    text:
                        type: string
                        description: Fulltext US street address
        default:
            description: Unexpected error
            schema:
                id: Error
                required:
                    - code
                    - message
                properties:
                    code:
                        type: integer
                        format: int32
                        example: 400
                    message:
                        type: string
                        description: Error message
                        example: Invalid or Missing JSON Request

    parameters:
        - in: body
          name: source
          schema:
              required:
                  - source
              id: Input
              properties:
                  source:
                      type: string
                      description: String to parse
                      example: >
                                 NOTICE IS HEREBY GIVEN, pursuant to law, that
                                 the New York City Department of Consumer
                                 Affairs will hold a Public Hearing on
                                 Wednesday, January 28, 2015, at 2:00 P.M., at
                                 66 John Street, 11th Floor, in the Borough of
                                 Manhattan, on the following petitions for
                                 sidewalk café revocable consent: 1. 132
                                 Mulberry Inc. 132 Mulberry Street in the
                                 Borough of Manhattan
    """
    if request.method == 'GET':
        return 'So, instructions would be printed here...'

    try:
        data = request.json
        source = data['source']
        ret = parseAddresses(source)
    except:
        errmsg = 'Invalid or Missing JSON Request'
        ret = jsonify({'code': 400, 'message': errmsg})

    return ret


@app.route('/spec')
def spec():
    swag = swagger(app)
    swag['info']['version'] = '0.1'
    swag['info']['title'] = "BetaNYC 5 Borough's address finder"
    return jsonify(swag)


@app.route('/api')
def apiroot():
    return app.send_static_file('index.html')


@app.route('/api/<path:path>')
def api(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)

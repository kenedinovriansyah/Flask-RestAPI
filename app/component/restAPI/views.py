import json
from six.moves.urllib.request import urlopen
from werkzeug.exceptions import HTTPException
from flask import url_for
from flask_jsonpify import jsonify
from flask_restplus import Namespace,Resource
from flask_api import status
from flask_api.decorators import set_renderers,set_parsers
from flask_api.renderers import JSONRenderer
from flask_api.parsers import JSONParser
from flask_cors import cross_origin

ns = Namespace('access',description='Main Api Country',validate=True)

@ns.route('/country')
class AccessCountry(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def get(self):
        try:
            load = urlopen('https://restcountries.eu/rest/v2/all?fields=name;')
            access = json.loads(load.read().decode())
            return jsonify(access),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

@ns.route('/image')
class AccessImage(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def get(self):
        try:
            dataimage = {}
            dataimage['image'] = url_for('static',filename='contentImage/' + "Transformer.jpg")
            dataimage['image1'] = url_for('static',filename='contentImage/' + 'SilentVoice.jpg')
            dataimage['image2'] = url_for('static',filename='contentImage/' + 'Yourname.jpg')
            dataimage['image3'] = url_for('static',filename='contentImage/' + 'plus.png')
            return jsonify(dataimage),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from flask_jsonpify import jsonify
from flask_restplus import Namespace,Resource,reqparse,fields
from flask_api import status
from flask_api.decorators import set_renderers,set_parsers
from flask_api.renderers import JSONRenderer
from flask_api.parsers import JSONParser
from flask_cors import cross_origin
from flask_praetorian import auth_required,roles_accepted,current_user
from app.database.models import User


authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

ns = Namespace('access',security='Bearer Auth', authorizations=authorizations)

reset_user = ns.model('Create Code', {
    'email': fields.String
})

access_user = ns.model('Access User',{
    'email': fields.String,
    'password': fields.String
})

create_user = reqparse.RequestParser()
create_user.add_argument('username',type=str)
create_user.add_argument('email',type=str)
create_user.add_argument('profil',type=FileStorage,location='files')
create_user.add_argument('gender',type=str)
create_user.add_argument('country',type=str)
create_user.add_argument('work',type=str)
create_user.add_argument('education',type=str)
create_user.add_argument('answersv1',type=str)
create_user.add_argument('answersv2',type=str)
create_user.add_argument('password',type=str)

update_user = reqparse.RequestParser()
update_user.add_argument('username',type=str)
update_user.add_argument('email',type=str)
update_user.add_argument('profil',type=FileStorage,location='files')
update_user.add_argument('profil_header',type=FileStorage,location='files')
update_user.add_argument('profil_background',type=FileStorage,location='files')
update_user.add_argument('gender',type=str)
update_user.add_argument('country',type=str)
update_user.add_argument('work',type=str)
update_user.add_argument('education',type=str)

update_user.add_argument('change_answer',type=str)
update_user.add_argument('change_password',type=str)
update_user.add_argument('answersv1',type=str)
update_user.add_argument('answersv2',type=str)
update_user.add_argument('new_answersv1',type=str)
update_user.add_argument('new_answersv2',type=str)
update_user.add_argument('oldpassword',type=str)
update_user.add_argument('newpassword',type=str)


@ns.route('/user/register')
class AccessCreateUser(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def post(self):
        try:
            args = create_user.parse_args()
            access = User.create_user(args)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

@ns.route('/user')
@ns.expect(access_user)
class AccessUser(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def post(self):
        try:
            access = User.access_user(ns.payload)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
            return jsonify({'message': True}),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

@ns.route('/user/<string:token>')
class AccessTokenUser(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    @auth_required
    @roles_accepted('operator','admin')
    def get(self,token):
        try:
            access = User.get_data_user(token)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    @auth_required
    @roles_accepted('admin','operator')
    def put(self,token):
        try:
            args = update_user.parse_args()
            user = current_user()
            access = User.put_user(user,token,args)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
            return jsonify({'message': True}),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def delete(self,token):
        try:
            access = User.delete_user(token)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

@ns.route('/uset/reset')
@ns.expect(reset_user)
class AccessResetUser(Resource):
    @cross_origin(headers=['Content-Type'])
    @set_renderers(JSONRenderer)
    @set_parsers(JSONParser)
    def post(self):
        try:
            access = User.reset_user(ns.payload)
            if not access:
                return jsonify({'message': False}),status.HTTP_400_BAD_REQUEST
            return jsonify(access),status.HTTP_200_OK
            return jsonify({'message': True}),status.HTTP_200_OK
        except HTTPException as e:
            return jsonify({'message': False}),status.HTTP_404_NOT_FOUND

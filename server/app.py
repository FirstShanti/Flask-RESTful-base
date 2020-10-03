import os
import json
import logging
import traceback

from pprint import pprint
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass

from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from validators import User_Validator
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from config import env
from utils import encrypt_string

logging.basicConfig(filename="server.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
server_log = logging.getLogger('server')


app = Flask(__name__)
app.config.from_object(env.get(os.environ.get('ENVIRONMENT')))

db = SQLAlchemy(app)
api = Api(app, prefix='/api/v1')
parser = reqparse.RequestParser(bundle_errors=True)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=uuid4().__str__(), unique=True)

    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(129), nullable=False, unique=True)
    phonenumber = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(256), nullable=False)

    remember_me = db.Column(db.Boolean, default=0)

    created = db.Column(db.DateTime, default=datetime.utcnow())
    last_login = db.Column(db.DateTime)

    authenticated = db.Column(db.Boolean, default=0)
    auth_key = db.Column(db.String(256))
    auth_key_created_at = db.Column(db.DateTime)

    access_rights = db.Column(db.String(32), default='user')


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        print('created: ', self.created)
        self.get_auth_key()
        self.hash_password()

    def hash_password(self):
        self.password = encrypt_string(self.username + self.password + datetime.utcnow().isoformat())


    def get_auth_key(self):
        self.auth_key = encrypt_string(f'{self.firstname} \
                                         {self.lastname} \
                                         {self.password} \
                                         {self.created}')
        self.auth_key_created_at = self.created

    def send_email_verification(self):
        print('send_email_verification')
        pass

    def serialize(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, datetime) else value

    @property
    def to_json(self):
        public_fields = [
            'uuid',
            'firstname',
            'lastname',
            'username',
            'email',
            'phonenumber',
            'created',
            'last_login',
            'access_rights'
        ]
        return dict(zip(
                [column for column in public_fields],
                [value_ for field in public_fields \
                    if (value_:= self.serialize(self.__dict__.get(field)))]
            ))

    def __repr__(self):
        return self.to_json


def args_to_parser(params, location):
    parser.args.clear()
    for field, valid_param in User_Validator[params].items():
        parser.add_argument(field, **valid_param, location=location)
    return parser


class Users(Resource):

    """
        Users endpoint: GET, CREATE, DELETE
    """

    def get(self, uuid=None):
        if uuid:
            user = User.query.filter_by(uuid=uuid).first_or_404()
            server_log.error(f'get user.__dict__: {user.__dict__}')
            server_log.error(f'get user.to_json: {user.to_json}')
            if user:
                return {'status': 'success', 'data': user.to_json}, 200
        
        parser = args_to_parser('page_limit', 'args')

        page = parser.parse_args().get('page')
        limit = parser.parse_args().get('limit')

        if str(page).isdigit():
            page = int(page)
        else:
            page = 1
        if str(limit).isdigit():
            limit = int(limit)
            if limit > 100:
                limit = 100
        else:
            limit = 20

        users = db.session.query(User).all()
        data = [user.to_json for user in users][page-1:page-1+limit]
        is_next = bool(users[page-1+limit:])

        return {'status': 'success', 'data': data, 'page': page, 'limit': limit, 'next': is_next}, 200


    def post(self):
        parser = args_to_parser('register', 'json')
        if (data:= parser.parse_args()):
            if not User.query.filter(
                User.username == data['username'],
                User.email == data['email']).first():
                
                user = User(**data)
                try:
                    db.session.add(user)
                    db.session.commit()
                    server_log.info(f'create: {user.uuid}')
                except:
                    server_log.error(f'not created: {traceback.format_exc()}')
                else:
                    user.send_email_verification()
                    return {'status': 'success', 'message': 'created', 'data': user.to_json}, 201
            return {'status': 'error', 'message': 'user exist'}, 404
        return {'status': 'error', 'message': 'invalid data'}, 404


    def put(self, uuid=None):
        parser = args_to_parser('update', 'json')
        if uuid and (uuid_:= UUID(uuid).__str__()):
            if (user:= db.session.query(User).filter_by(uuid=uuid).first_or_404()):
                if (data:= parser.parse_args()):
                    for field, value in data.items():
                        if value:
                            setattr(user, field, value)
                    data = user.to_json
                    try:
                        db.session.commit()
                    except:
                        server_log.error(f'not seve: {traceback.format_exc()}')
                    return {'status': 'success', 'message': 'updated', 'data': data}, 200
                return {'status': 'error', 'message': 'request body is empty'}, 400
            return {'status': 'error', 'message': 'user not found'}, 400
        return {'status': 'error', 'message': 'invalid uuid'}, 400


    def delete(self, uuid=None):
        if uuid and (uuid_:= UUID(uuid)):
            if (user:= User.query.filter_by(uuid=uuid_.__str__()).first_or_404()):
                db.session.delete(user)
                db.session.commit()
                return {'status': 'success', 'message': 'user deleted'}, 204
        return {'status': 'error', 'message': 'invalid uuid'}, 400


# # RESOURCES
# class UserLogin(Resource):
#     """
#         Login User with created access and refresh token
#     """
#     parser = reqparse.RequestParser()
#     for field, valid_param in User_Validator['login'].items():
#         parser.add_argument(field, *valid_param)

#     def post(self):
#         data = parser.parser_args()
#         user = User_Model.query.filter(User.username==data.get('username'))

#         if user and safe_str_cmp(user.password, data.get('password')):
#             access_token = create_access_token(identity=user.uuid, fresh=True)
#             refresh_token = create_refresh_token(user.uuid)
#             return {
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#                 }, 200

#         return {'message': 'Invalid credentials!'}, 401


# api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/users', '/users/<string:uuid>')

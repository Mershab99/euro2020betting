from flask_restful import Resource, reqparse

from src.common.constants import ADMIN_USERNAME, ADMIN_PASSWORD
from src.core.managers.mgr_user import create_user


class CreateUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name", type=str, location='json')
    parser.add_argument("last_name", type=str, location='json')
    parser.add_argument("teams", type=list, location='json')
    parser.add_argument("player", type=str, location='json')

    def post(self):
        data = self.parser.parse_args()
        try:
            create_user(first_name=data['first_name'], last_name=data['last_name'], teams=data['teams'],
                        player=data['player'])
            return {
                'message': 'success'
            }
        except Exception:
            return {
                'message': 'failure'
            }


class Delete(Resource):
    @staticmethod
    def get():
        return {
            'test': True
        }


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, location='json')
    parser.add_argument("password", type=str, location='json')

    def post(self):
        data = self.parser.parse_args()
        if data['username'] == ADMIN_USERNAME and data['password'] == ADMIN_PASSWORD:
            return {
                'message': 'success'
            }
        else:
            return {
                'message': 'failure'
            }

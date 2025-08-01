from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        data = request.json
        user = facade.get_user_by_email(data['email'])
        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200

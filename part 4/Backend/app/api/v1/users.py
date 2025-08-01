from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth import admin_required

api = Namespace('users', description='Operations related to users')

user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='User ID'),
    'first_name': fields.String(required=True, description='User\'s first name'),
    'last_name': fields.String(required=True, description='User\'s last name'),
    'email': fields.String(required=True, description='User\'s email address'),
    'password': fields.String(required=True, description='User\'s password', writeOnly=True)
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(readOnly=True, description='User ID'),
    'first_name': fields.String(description='User\'s first name'),
    'last_name': fields.String(description='User\'s last name'),
    'email': fields.String(description='User\'s email address'),
})

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user = get_jwt_identity()
        user_data = request.json
        
        if current_user.get('is_admin', False):
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return updated_user.to_dict(), 200

        if user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400
            
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return updated_user.to_dict(), 200

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """Retrieve the list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid data')
    @jwt_required()
    @admin_required
    def post(self):
        """Register a new user (public endpoint)"""
        user_data = request.json
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

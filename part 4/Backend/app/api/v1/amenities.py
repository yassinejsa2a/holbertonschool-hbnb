from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth import admin_required

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'Liste des commodités')
    def get(self):
        """Obtenir la liste de toutes les commodités"""
        amenities = facade.get_all_amenities()
        return [vars(amenity) for amenity in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Commodité créée')
    @jwt_required()
    @admin_required
    def post(self):
        """Créer une nouvelle commodité (Admin only)"""
        data = api.payload
        new_amenity = facade.create_amenity(data)
        return vars(new_amenity), 201

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'ID de la commodité')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Retrieve a specific amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return vars(amenity)

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Commodité mise à jour')
    @api.response(404, 'Commodité non trouvée')
    @jwt_required()
    @admin_required
    def put(self, amenity_id):
        """Mettre à jour une commodité (Admin only)"""
        updated = facade.update_amenity(amenity_id, api.payload)
        if not updated:
            return {'error': 'Commodité non trouvée'}, 404
        return vars(updated), 200

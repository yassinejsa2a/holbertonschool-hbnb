from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Endpoints for managing reviews')
facade = HBnBFacade()

review_model = api.model('Review', {
    'id': fields.String(readOnly=True, description='Unique review ID'),
    'text': fields.String(required=True, description='Review content'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(readOnly=True, description='ID of the user'),  # Changed to readOnly
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [vars(review) for review in reviews], 200

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        data = api.payload
        current_user = get_jwt_identity()
        data['user_id'] = current_user['id']
        place = facade.get_place(data['place_id'])
        if not place:
            api.abort(400, "Place not found")
        if place.owner_id == current_user['id']:
            api.abort(400, "You cannot review your own place")
        # Check if user already reviewed this place
        reviews = facade.get_reviews_by_place(data['place_id'])
        for review in reviews:
            if review.user_id == current_user['id']:
                api.abort(400, "You have already reviewed this place")
        review = facade.create_review(data)
        return vars(review), 201

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by its ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return vars(review)

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        if not is_admin and review.user_id != current_user['id']:
            api.abort(403, "Unauthorized action")
        data = api.payload
        if 'user_id' in data or 'place_id' in data:
            api.abort(400, "You cannot modify user_id or place_id")
        review = facade.update_review(review_id, data)
        return vars(review)

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        if not is_admin and review.user_id != current_user['id']:
            api.abort(403, "Unauthorized action")
        result = facade.delete_review(review_id)
        return {'message': 'Review deleted'}, 200

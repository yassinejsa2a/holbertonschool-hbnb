import unittest
import uuid
from app import create_app, db
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade

class TestReview(unittest.TestCase):
    """Test cases for Review model"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Créer l'application Flask avec contexte
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer les tables
        db.create_all()
        
        self.review_data = {
            'text': 'Great place to stay!',
            'rating': 5,
            'user_id': str(uuid.uuid4()),
            'place_id': str(uuid.uuid4())
        }
        
        self.review = Review(
            id=str(uuid.uuid4()),
            text=self.review_data['text'],
            rating=self.review_data['rating'],
            user_id=self.review_data['user_id'],
            place_id=self.review_data['place_id']
        )

    def tearDown(self):
        """Tear down test fixtures after each test method"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_review_creation(self):
        """Test review creation with valid data"""
        self.assertEqual(self.review.text, 'Great place to stay!')
        self.assertEqual(self.review.rating, 5)
        self.assertIsNotNone(self.review.id)

    def test_review_attributes(self):
        """Test review attributes are correctly set"""
        self.assertEqual(self.review.text, 'Great place to stay!')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.user_id, self.review_data['user_id'])
        self.assertEqual(self.review.place_id, self.review_data['place_id'])
        self.assertIsInstance(self.review.id, str)

    def test_review_rating_validation_valid(self):
        """Test review rating validation with valid values"""
        for rating in [1, 2, 3, 4, 5]:
            review = Review(
                id=str(uuid.uuid4()),
                text='Test review',
                rating=rating,
                user_id=str(uuid.uuid4()),
                place_id=str(uuid.uuid4())
            )
            self.assertEqual(review.rating, rating)

    def test_review_rating_validation_invalid_low(self):
        """Test review rating validation with invalid low value"""
        with self.assertRaises(ValueError):
            Review(
                id=str(uuid.uuid4()),
                text='Test review',
                rating=0,
                user_id=str(uuid.uuid4()),
                place_id=str(uuid.uuid4())
            )

    def test_review_rating_validation_invalid_high(self):
        """Test review rating validation with invalid high value"""
        with self.assertRaises(ValueError):
            Review(
                id=str(uuid.uuid4()),
                text='Test review',
                rating=6,
                user_id=str(uuid.uuid4()),
                place_id=str(uuid.uuid4())
            )

    def test_review_update(self):
        """Test review update method"""
        update_data = {
            'text': 'Updated review text',
            'rating': 4
        }
        self.review.update(update_data)
        
        self.assertEqual(self.review.text, 'Updated review text')
        self.assertEqual(self.review.rating, 4)

    def test_review_update_with_validation(self):
        """Test review update with validation"""
        with self.assertRaises(ValueError):
            self.review.update({'rating': 0})

    def test_review_id_unique(self):
        """Test that review IDs are unique"""
        review1 = Review(
            text='Review 1',
            rating=5,
            user_id=str(uuid.uuid4()),
            place_id=str(uuid.uuid4())
        )
        review2 = Review(
            text='Review 2',
            rating=4,
            user_id=str(uuid.uuid4()),
            place_id=str(uuid.uuid4())
        )
        self.assertNotEqual(review1.id, review2.id)


class TestReviewFacade(unittest.TestCase):
    """Test cases for Review operations through facade"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Créer l'application Flask avec contexte
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer les tables
        db.create_all()
        
        self.facade = HBnBFacade()
        
        # Créer un utilisateur pour les tests
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword123'
        }
        self.user = self.facade.create_user(self.user_data)
        
        # Créer un autre utilisateur (propriétaire)
        self.owner_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'anotherpassword123'
        }
        self.owner = self.facade.create_user(self.owner_data)
        
        # Créer un lieu
        self.place_data = {
            'title': 'Beautiful Apartment',
            'description': 'A lovely place to stay',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.owner.id,
            'amenities': []
        }
        self.place = self.facade.create_place(self.place_data)
        
        self.review_data = {
            'text': 'Great place to stay!',
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        }

    def tearDown(self):
        """Tear down test fixtures after each test method"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_review_facade(self):
        """Test review creation through facade"""
        review = self.facade.create_review(self.review_data)
        self.assertIsNotNone(review)
        self.assertEqual(review.text, 'Great place to stay!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, self.user.id)
        self.assertEqual(review.place_id, self.place.id)

    def test_get_review_facade(self):
        """Test getting review by ID through facade"""
        created_review = self.facade.create_review(self.review_data)
        retrieved_review = self.facade.get_review(created_review.id)
        
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review.id, created_review.id)
        self.assertEqual(retrieved_review.text, created_review.text)

    def test_get_all_reviews_facade(self):
        """Test getting all reviews through facade"""
        review1 = self.facade.create_review(self.review_data)
        review2_data = self.review_data.copy()
        review2_data['text'] = 'Another great review!'
        review2_data['rating'] = 4
        review2 = self.facade.create_review(review2_data)
        
        all_reviews = self.facade.get_all_reviews()
        self.assertEqual(len(all_reviews), 2)
        self.assertIn(review1, all_reviews)
        self.assertIn(review2, all_reviews)

    def test_update_review_facade(self):
        """Test updating review through facade"""
        created_review = self.facade.create_review(self.review_data)
        update_data = {
            'text': 'Updated review text',
            'rating': 4
        }
        
        updated_review = self.facade.update_review(created_review.id, update_data)
        
        self.assertIsNotNone(updated_review)
        self.assertEqual(updated_review.text, 'Updated review text')
        self.assertEqual(updated_review.rating, 4)

    def test_delete_review_facade(self):
        """Test deleting review through facade"""
        created_review = self.facade.create_review(self.review_data)
        result = self.facade.delete_review(created_review.id)
        
        self.assertTrue(result)
        deleted_review = self.facade.get_review(created_review.id)
        self.assertIsNone(deleted_review)

    def test_get_reviews_by_place_facade(self):
        """Test getting reviews by place through facade"""
        review1 = self.facade.create_review(self.review_data)
        
        # Créer un autre lieu et un avis pour ce lieu
        place2_data = self.place_data.copy()
        place2_data['title'] = 'Another Place'
        place2 = self.facade.create_place(place2_data)
        
        review2_data = self.review_data.copy()
        review2_data['place_id'] = place2.id
        review2 = self.facade.create_review(review2_data)
        
        place1_reviews = self.facade.get_reviews_by_place(self.place.id)
        self.assertEqual(len(place1_reviews), 1)
        self.assertIn(review1, place1_reviews)
        self.assertNotIn(review2, place1_reviews)

    def test_create_review_invalid_rating(self):
        """Test creating review with invalid rating"""
        invalid_review_data = self.review_data.copy()
        invalid_review_data['rating'] = 6  # Invalid rating
        
        with self.assertRaises(ValueError):
            self.facade.create_review(invalid_review_data)

    def test_get_nonexistent_review(self):
        """Test getting a review that doesn't exist"""
        fake_id = str(uuid.uuid4())
        review = self.facade.get_review(fake_id)
        self.assertIsNone(review)

    def test_update_nonexistent_review(self):
        """Test updating a review that doesn't exist"""
        fake_id = str(uuid.uuid4())
        update_data = {'text': 'Updated text'}
        result = self.facade.update_review(fake_id, update_data)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

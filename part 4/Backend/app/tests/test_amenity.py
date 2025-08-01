import unittest
import uuid
from app import create_app, db
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade

class TestAmenity(unittest.TestCase):
    """Test cases for Amenity model"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Créer l'application Flask avec contexte
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer les tables
        db.create_all()
        
        self.amenity_data = {
            'name': 'WiFi'
        }
        
        self.amenity = Amenity(
            id=str(uuid.uuid4()),
            name=self.amenity_data['name']
        )

    def tearDown(self):
        """Tear down test fixtures after each test method"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_amenity_creation(self):
        """Test amenity creation with valid data"""
        self.assertEqual(self.amenity.name, 'WiFi')
        self.assertIsNotNone(self.amenity.id)

    def test_amenity_attributes(self):
        """Test amenity attributes are correctly set"""
        self.assertEqual(self.amenity.name, 'WiFi')
        self.assertIsInstance(self.amenity.id, str)

    def test_amenity_name_required(self):
        """Test that amenity name is required"""
        with self.assertRaises(ValueError):
            Amenity(
                id=str(uuid.uuid4()),
                name=''  # Empty name should raise error
            )

    def test_amenity_update(self):
        """Test amenity update method"""
        update_data = {'name': 'High-Speed WiFi'}
        self.amenity.update(update_data)
        self.assertEqual(self.amenity.name, 'High-Speed WiFi')

    def test_amenity_id_unique(self):
        """Test that amenity IDs are unique"""
        amenity1 = Amenity(name='WiFi')
        amenity2 = Amenity(name='Parking')
        self.assertNotEqual(amenity1.id, amenity2.id)


class TestAmenityFacade(unittest.TestCase):
    """Test cases for Amenity operations through facade"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Créer l'application Flask avec contexte
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer les tables
        db.create_all()
        
        self.facade = HBnBFacade()
        self.amenity_data = {
            'name': 'WiFi'
        }

    def tearDown(self):
        """Tear down test fixtures after each test method"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_amenity_facade(self):
        """Test amenity creation through facade"""
        amenity = self.facade.create_amenity(self.amenity_data)
        self.assertIsNotNone(amenity)
        self.assertEqual(amenity.name, 'WiFi')

    def test_get_amenity_facade(self):
        """Test getting amenity by ID through facade"""
        created_amenity = self.facade.create_amenity(self.amenity_data)
        retrieved_amenity = self.facade.get_amenity(created_amenity.id)
        
        self.assertIsNotNone(retrieved_amenity)
        self.assertEqual(retrieved_amenity.id, created_amenity.id)
        self.assertEqual(retrieved_amenity.name, created_amenity.name)

    def test_get_all_amenities_facade(self):
        """Test getting all amenities through facade"""
        amenity1 = self.facade.create_amenity(self.amenity_data)
        amenity2_data = {'name': 'Parking'}
        amenity2 = self.facade.create_amenity(amenity2_data)
        
        all_amenities = self.facade.get_all_amenities()
        self.assertEqual(len(all_amenities), 2)
        self.assertIn(amenity1, all_amenities)
        self.assertIn(amenity2, all_amenities)

    def test_update_amenity_facade(self):
        """Test updating amenity through facade"""
        created_amenity = self.facade.create_amenity(self.amenity_data)
        update_data = {'name': 'High-Speed WiFi'}
        
        updated_amenity = self.facade.update_amenity(created_amenity.id, update_data)
        
        self.assertIsNotNone(updated_amenity)
        self.assertEqual(updated_amenity.name, 'High-Speed WiFi')

    def test_delete_amenity_facade(self):
        """Test deleting amenity through facade"""
        created_amenity = self.facade.create_amenity(self.amenity_data)
        result = self.facade.delete_amenity(created_amenity.id)
        
        self.assertTrue(result)
        deleted_amenity = self.facade.get_amenity(created_amenity.id)
        self.assertIsNone(deleted_amenity)

    def test_get_nonexistent_amenity(self):
        """Test getting an amenity that doesn't exist"""
        fake_id = str(uuid.uuid4())
        amenity = self.facade.get_amenity(fake_id)
        self.assertIsNone(amenity)

    def test_update_nonexistent_amenity(self):
        """Test updating an amenity that doesn't exist"""
        fake_id = str(uuid.uuid4())
        update_data = {'name': 'Updated Name'}
        result = self.facade.update_amenity(fake_id, update_data)
        self.assertIsNone(result)

    def test_create_multiple_amenities_different_names(self):
        """Test creating multiple amenities with different names"""
        amenities_data = [
            {'name': 'WiFi'},
            {'name': 'Parking'},
            {'name': 'Pool'},
            {'name': 'Gym'}
        ]
        
        created_amenities = []
        for data in amenities_data:
            amenity = self.facade.create_amenity(data)
            created_amenities.append(amenity)
        
        self.assertEqual(len(created_amenities), 4)
        
        # Vérifier que tous les noms sont différents
        names = [amenity.name for amenity in created_amenities]
        self.assertEqual(len(names), len(set(names)))  # Pas de doublons


if __name__ == '__main__':
    unittest.main()

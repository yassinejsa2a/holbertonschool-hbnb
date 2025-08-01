#!/usr/bin/env python3
"""
Script pour initialiser la base de données et créer les tables
"""

from app import create_app, db
from app.models import User, Place, Review, Amenity
import uuid

def init_database():
    """Initialise la base de données et crée les tables"""
    app = create_app()
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("Tables créées avec succès!")
        
        # Créer un utilisateur administrateur
        admin_id = str(uuid.uuid4())
        admin = User(
            id=admin_id,
            email='admin@hbnb.com',
            password='admin1234',
            first_name='Admin',
            last_name='User'
        )
        
        # Vérifier si l'admin existe déjà
        existing_admin = User.query.filter_by(email='admin@hbnb.com').first()
        if not existing_admin:
            db.session.add(admin)
            print("Utilisateur administrateur créé!")
        else:
            print("Utilisateur administrateur existe déjà!")
        
        # Créer un utilisateur lambda (non-admin)
        jane_id = str(uuid.uuid4())
        jane = User(
            id=jane_id,
            email='jane@example.com',
            password='password123',
            first_name='Jane',
            last_name='Doe'
        )
        
        # Vérifier si Jane existe déjà
        existing_jane = User.query.filter_by(email='jane@example.com').first()
        if not existing_jane:
            db.session.add(jane)
            print("Utilisateur lambda Jane créé!")
        else:
            print("Utilisateur lambda Jane existe déjà!")
        
        # Créer des équipements de base
        amenities_data = [
            'WiFi', 'Parking', 'Air Conditioning', 'Kitchen',
            'Washing Machine', 'TV', 'Pool', 'Gym', 'Pet Friendly', 'Balcony'
        ]
        
        for amenity_name in amenities_data:
            existing_amenity = Amenity.query.filter_by(name=amenity_name).first()
            if not existing_amenity:
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
        
        # Créer 5 places de test avec des noms originaux
        print("\nCréation de 5 places de test avec des noms originaux...")
        
        # Récupérer les équipements pour les associer aux places
        wifi = Amenity.query.filter_by(name='WiFi').first()
        parking = Amenity.query.filter_by(name='Parking').first()
        pool = Amenity.query.filter_by(name='Pool').first()
        kitchen = Amenity.query.filter_by(name='Kitchen').first()
        gym = Amenity.query.filter_by(name='Gym').first()
        
        # Utiliser Jane comme propriétaire par défaut
        owner = existing_jane if existing_jane else jane
        admin_owner = existing_admin if existing_admin else admin
        
        test_places = [
            {
                'title': 'Annonce 1',
                'description': 'test test description test',
                'price': 89.99,
                'latitude': 45.764043,
                'longitude': 4.835659,
                'amenities': [wifi, kitchen] if wifi and kitchen else [],
                'owner': owner  # Jane
            },
            {
                'title': 'Annonce 2',
                'description': 'test test description test',
                'price': 49.00,
                'latitude': 43.604652,
                'longitude': 1.444209,
                'amenities': [wifi, parking, pool] if all([wifi, parking, pool]) else [],
                'owner': admin_owner  # Admin
            },
            {
                'title': 'Annonce 3',
                'description': 'test test description test',
                'price': 9.00,
                'latitude': 48.856614,
                'longitude': 2.352222,
                'amenities': [wifi, parking, pool, gym] if all([wifi, parking, pool, gym]) else [],
                'owner': owner  # Jane
            },
            {
                'title': 'Annonce 4',
                'description': 'test test description test',
                'price': 51.00,
                'latitude': -17.686995,
                'longitude': -149.426956,
                'amenities': [wifi, kitchen, pool] if all([wifi, kitchen, pool]) else [],
                'owner': owner  # Jane
            },
            {
                'title': 'Annonce 5',
                'description': 'test test description test',
                'price': 175.25,
                'latitude': 51.507351,
                'longitude': -0.127758,
                'amenities': [wifi, parking, gym, kitchen] if all([wifi, parking, gym, kitchen]) else [],
                'owner': owner  # Jane
            }
        ]
        
        created_places = []
        for place_data in test_places:
            # Vérifier si la place existe déjà
            existing_place = Place.query.filter_by(title=place_data['title']).first()
            if not existing_place:
                new_place = Place(
                    title=place_data['title'],
                    description=place_data['description'],
                    price=place_data['price'],
                    latitude=place_data['latitude'],
                    longitude=place_data['longitude'],
                    owner_id=place_data['owner'].id  # Utiliser le propriétaire spécifique
                )
                # Associer les équipements
                for amenity in place_data['amenities']:
                    if amenity:
                        new_place.amenities.append(amenity)
                
                db.session.add(new_place)
                created_places.append(new_place)
            else:
                print(f"Place '{place_data['title']}' existe déjà!")
        
        # Sauvegarder les changements
        db.session.commit()
        
        # Afficher les places créées
        for i, place in enumerate(created_places):
            print(f"✓ Place {i+1}: '{place.title}' créée (ID: {place.id})")
            print(f"  Prix: {place.price}€ - Équipements: {place.amenities.count()}")
        
        print("Données initiales insérées avec succès!")
        
        # Afficher un résumé
        print(f"\nRésumé:")
        print(f"Utilisateurs: {User.query.count()}")
        print(f"Équipements: {Amenity.query.count()}")
        print(f"Lieux: {Place.query.count()}")
        print(f"Avis: {Review.query.count()}")

if __name__ == '__main__':
    init_database()

from sqlalchemy import Table, Column, String, ForeignKey
from app import db

# Table d'association pour la relation Many-to-Many Place <-> Amenity
place_amenity = Table(
    'place_amenity',
    db.Model.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)

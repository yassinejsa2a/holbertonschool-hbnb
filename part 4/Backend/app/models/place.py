from app import db
from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from app.models.associations import place_amenity
import uuid

class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    
    # Relations
    reviews = relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary=place_amenity, back_populates='places', lazy='dynamic')
    
    def __init__(self, title, description, price, latitude, longitude, owner_id, id=None, amenities=None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner_id = owner_id
        
        # Gestion des amenities (sera géré après création)
        if amenities is not None:
            self._pending_amenities = amenities

    def _validate_price(self, price):
        """Validate that the price is positive"""
        if price < 0:
            raise ValueError("Price must be positive")
        return price

    def _validate_latitude(self, latitude):
        """Validate that latitude is between -90 and 90"""
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    def _validate_longitude(self, longitude):
        """Validate that longitude is between -180 and 180"""
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def update(self, data):
        """Update the attributes of the place"""
        for key, value in data.items():
            if key == 'price':
                value = self._validate_price(value)
            elif key == 'latitude':
                value = self._validate_latitude(value)
            elif key == 'longitude':
                value = self._validate_longitude(value)
            elif key == 'amenities':
                # Handle amenities separately
                continue
            setattr(self, key, value)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from this place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

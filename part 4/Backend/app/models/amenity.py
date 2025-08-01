from app import db
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from app.models.associations import place_amenity
import uuid

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    name = Column(String(50), unique=True, nullable=False)
    
    # Relation many-to-many avec Place
    places = relationship('Place', secondary=place_amenity, back_populates='amenities', lazy='dynamic')
    
    def __init__(self, name, id=None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        """Validate amenity name"""
        if not name or not name.strip():
            raise ValueError("Amenity name cannot be empty")
        if len(name.strip()) > 50:
            raise ValueError("Amenity name cannot be longer than 50 characters")
        return name.strip()

    def update(self, data):
        for key, value in data.items():
            if key == 'name':
                value = self._validate_name(value)
            setattr(self, key, value)

from app import db
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.models.base_model import BaseModel
import uuid

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    
    def __init__(self, text, rating, user_id, place_id, id=None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.text = text
        self.rating = self._validate_rating(rating)
        self.user_id = user_id
        self.place_id = place_id

    def _validate_rating(self, rating):
        """Validate that rating is between 1 and 5"""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def update(self, data):
        """Update the attributes of the review"""
        for key, value in data.items():
            if key == 'rating':
                value = self._validate_rating(value)
            setattr(self, key, value)

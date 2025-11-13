from sqlalchemy.sql import func
from config import db

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'<Category {self.name}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }


from sqlalchemy.sql import func
from config import db

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150) , nullable=False)
    name = db.Column(db.String(100) , nullable=False)
    password = db.Column(db.String(500) , nullable=False)
    contact = db.Column(db.String(200) , nullable=False)
    address = db.Column(db.String(500) , nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default = func.now())
    # def __init__(self, email, name, password, contact, address):
    #     self.email = email
    #     self.name = name
    #     self.password =  password
    #     self.contact = contact
    #     self.address = address

    # def __repr__(self):
    #     return '<User %r>' % self.name
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'email': self.email,
    #         'name': self.name,
    #         'password':  self.password,
    #         'contact': self.contact,
    #         'address': self.address,
    #         'created_at': self.created_at
    #     }
    
from sqlalchemy.sql import func #type: ignore
from config import db

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150) , nullable=False)
    name = db.Column(db.String(100) , nullable=False)
    password = db.Column(db.String(500) , nullable=False)
    contact = db.Column(db.String(200) , nullable=False)
    address = db.Column(db.String(500) , nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean , default=False)
    # city = db.Column(db.String(100))
    # country = db.Column(db.String(100))
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime(timezone=True), default = func.now())
    # orders = db.relationship('Order', backref='customer', lazy=True)
    # carts = db.relationship('Cart', backref='customer', lazy=True)

    def is_admin(self):
        return self.role == 'admin'
    def __init__(self, email, name, password, contact, address,role):
        self.email = email
        self.name = name
        self.password =  password
        self.contact = contact
        self.address = address
        self.role = role  # 'user' or 'admin'
        
    def __repr__(self):
        return '<User %r>' % self.name
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'password':  self.password,
            'contact': self.contact,
            'address': self.address,
            'role': self.role,  # 'user' or 'admin'  # 'user' or 'admin'
            'created_at': self.created_at
        }
    
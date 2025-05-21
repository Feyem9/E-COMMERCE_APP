from sqlalchemy.sql import func #type:ignore
from config import db

class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer , nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(40) , nullable=False)
    product_description = db.Column(db.String(255) , nullable=True)
    product_image = db.Column(db.String(255) , nullable=True)
    current_price = db.Column(db.Integer , nullable=True)
    product = db.relationship('Products', backref=db.backref('carts', lazy=True))
    customer_id = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default = func.now())

    def __init__(self, quantity, product_id,product_name, product_description=None , product_image=None , current_price=None , customer_id=None):
        self.quantity = quantity
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.product_image = product_image
        self.current_price = current_price
        self.customer_id = customer_id
    def __repr__(self):
        return '<User %r>' % self.id
    def serialize(self):
        return {
            'quantity': self.quantity,
            'product_id': self.product_id,
            'product_description': self.product_description,
            'product_image': self.product_image,
            'current_price': self.current_price,
            'created_at': self.created_at
        }
    
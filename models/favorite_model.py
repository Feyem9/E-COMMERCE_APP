# from sqlalchemy.sql import func
# from config import db

# class Favorites(db.model):
#     id = db.Column(db.Integer , primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
#     customer = db.relationship('Customers', backref=db.backref('favorites', lazy=True))
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
#     product = db.relationship('Products', backref=db.backref('favorites', lazy=True))
#     created_at = db.Column(db.DateTime(timezone=True), default = func.now())

#     # def __init__(self, customer_id, product_id):
#     #     self.customer_id = customer_id
#     #     self.product_id = product_id
#     # def __repr__(self):
#     #     return '<User %r>' % self.name
#     # def serialize(self):
#     #     return {
#     #         'id': self.id,
#     #         'customer_id': self.customer_id,
#     #         'product_id': self.product_id,
#     #         'created_at': self.created_at
#     #     }
# from sqlalchemy.sql import func
# from config import db

# class Orders(db.model):
#     id = db.Column(db.Integer , primary_key=True)
#     quantity = db.Column(db.Integer , nullable=False)
#     price = db.Column(db.Float , nullable=False)
#     status = db.Column(db.String(100) , nullable=False)
#     cart_id = db.Column(db.Integer , db.ForeignKey('carts.id'))
#     cart = db.relationship('Carts', backref=db.backref('orders', lazy=True))
#     created_at = db.Column(db.DateTime(timezone=True), default = func.now())
#     # def __init__(self, quantity, price, status, cart_id):
#     #     self.quantity = quantity
#     #     self.price = price
#     #     self.status = status
#     #     self.cart_id = cart_id
#     # def __repr__(self):
#     #     return '<User %r>' % self.name
#     # def serialize(self):
#     #     return {
#     #         'id': self.id,
#     #         'quantity': self.quantity,
#     #         'price': self.price,
#     #         'status': self.status,
#     #         'cart_id': self.cart_id,
#     #         'created_at': self.created_at
#     #     }
    
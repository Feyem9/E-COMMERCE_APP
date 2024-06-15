# from sqlalchemy.sql import func
# from config import db

# class Transactions(db.model):
#     id = db.Column(db.Integer , primary_key=True)
#     status = db.Column(db.String(255))
#     order_id = db.Column(db.Integer , db.ForiegnKey('orders.id'))
#     order = db.relationship('Orders', backref=db.backref('transactions', lazy=True))
#     created_at = db.Column(db.DateTime(timezone=True), default = func.now())

#     # def __init__(self, order_id):
#     #     self.order_id = order_id
#     # def __repr__(self):
#     #     return '<User %r>' % self.name
#     # def serialize(self):
#     #     return {
#     #         'id': self.id,
#     #         'order_id': self.order_id,
#     #         'created_at': self.created_at
#     #     }

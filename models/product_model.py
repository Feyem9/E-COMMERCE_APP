# from sqlalchemy.sql import func
# from config import db

# class Products(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100) , nullable=False)
#     description = db.Column(db.String(100) , nullable=False)
#     current_price = db.Column(db.Float , nullable=False)
#     discount_price = db.Column(db.Float , nullable=False)
#     quantity = db.Column(db.Integer , nullable=False)
#     picture = db.Column(db.String(2000), nullable=False)
#     flash_sale = db.Column(db.Boolean , nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), default = func.now())
    
#     # def __init__(self, name, description, current_price, discount_price, quantity, picture, flash_sale):
#     #     self.name = name
#     #     self.description = description
#     #     self.current_price = current_price
#     #     self.discount_price = discount_price
#     #     self.quantity = quantity
#     #     self.picture = picture
#     #     self.flash_sale = flash_sale

#     # def __repr__(self):
#     #     return '<User %r>' % self.name
    
#     # def serialize(self):
#     #     return {
#     #         'id': self.id,
#     #         'name': self.name,
#     #         'description': self.description,
#     #         'current_price': self.current_price,
#     #         'discount_price': self.discount_price,
#     #         'quantity': self.quantity,
#     #         'picture': self.picture,
#     #         'flash_sale': self.flash_sale,
#     #         'created_at': self.created_at
#     #     }
    
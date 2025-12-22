from sqlalchemy.sql import func  # type: ignore
from config import db

class Transactions(db.Model):
    transaction_id = db.Column('transaction_id' ,db.String(100), primary_key=True)
    status = db.Column(db.String(255))
    total_amount = db.Column(db.Integer)
    currency = db.Column(db.String(255))
    redirect_url = db.Column(db.String(255))
    # order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    # order = db.relationship('Orders', backref=db.backref('transactions', lazy=True))
    
    # ✅ Géolocalisation
    customer_latitude = db.Column(db.Float, nullable=True)
    customer_longitude = db.Column(db.Float, nullable=True)
    delivery_distance_km = db.Column(db.Float, nullable=True)
    delivery_map_url = db.Column(db.String(500), nullable=True)  # 🗺️ Lien Google Maps
    
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, status, transaction_id, total_amount, currency, redirect_url=None, 
                 customer_latitude=None, customer_longitude=None, delivery_distance_km=None,
                 delivery_map_url=None):
        self.status = status
        self.transaction_id = transaction_id
        self.total_amount = total_amount
        self.currency = currency
        self.redirect_url = redirect_url
        self.customer_latitude = customer_latitude
        self.customer_longitude = customer_longitude
        self.delivery_distance_km = delivery_distance_km
        self.delivery_map_url = delivery_map_url

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'

    def serialize(self):
        return {
            'transaction_id': self.transaction_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'redirect_url': self.redirect_url,
            'customer_latitude': self.customer_latitude,
            'customer_longitude': self.customer_longitude,
            'delivery_distance_km': self.delivery_distance_km,
            'delivery_map_url': self.delivery_map_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


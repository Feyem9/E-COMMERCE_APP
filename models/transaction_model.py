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
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, status ,transaction_id , total_amount , currency , redirect_url=None):
        self.status = status
        self.transaction_id = transaction_id
        self.total_amount = total_amount
        self.currency = currency
        self.redirect_url = redirect_url

    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'

    def serialize(self):
        return {
            'transaction_id': self.transaction_id,
            'status': self.status,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'redirect_url': self.redirect_url,
            # 'order_id': self.order_id,
            # 'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


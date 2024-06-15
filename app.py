from flask import Flask
from flask_migrate import Migrate

from config import db, SECRET_KEY

from routes.customer_route import customer
# from routes.cart_route import cart
# from routes.categoriy_route import category
# from routes.favorite_route import favorite
# from routes.order_route import order
# from routes.product_route import product
# from routes.transaction_route import transaction


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = SECRET_KEY

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(customer , url_prefix='/')
# app.register_blueprint(cart , url_prefix='/cart')
# app.register_blueprint(category , url_prefix='/category')
# app.register_blueprint(favorite , url_prefix='/favorite')
# app.register_blueprint(order , url_prefix='/order')
# app.register_blueprint(product , url_prefix='/product')
# app.register_blueprint(transaction , url_prefix='/transaction')

if __name__ == '__main__':
    app.run(debug=True)
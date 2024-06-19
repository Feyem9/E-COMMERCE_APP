from flask import Flask , request
from flask_migrate import Migrate
from flask_mail import Mail , Message

from config import db, SECRET_KEY , MAIL_SERVER , MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD,MAIL_USE_SSL,MAIL_USE_TLS

from models.customer_model import Customers

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
app.MAIL_SERVER = MAIL_SERVER
app.MAIL_PORT = MAIL_PORT
app.MAIL_USERNAME = MAIL_USERNAME
app.MAIL_PASSWORD = MAIL_PASSWORD
app.MAIL_USE_SSL = MAIL_USE_SSL
app.MAIL_USE_TLS = MAIL_USE_TLS

mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(customer , url_prefix='/')
# app.register_blueprint(cart , url_prefix='/cart')
# app.register_blueprint(category , url_prefix='/category')
# app.register_blueprint(favorite , url_prefix='/favorite')
# app.register_blueprint(order , url_prefix='/order')
# app.register_blueprint(product , url_prefix='/product')
# app.register_blueprint(transaction , url_prefix='/transaction')

@app.route('/mail')
def index():
    email = request.form.get('email')
    customer = Customers.query.filter_by(email=email).first()
    print(customer)
    msg = Message(subject='Hello from the other side!', sender='feyemlionel@gmail.com', recipients=['christiandongueu61@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask-ecommerce-app, lmk if it works"
    # print(msg)
    mail.send(msg)
    return "Message sent ok!"

if __name__ == '__main__':
    app.run(debug=True)
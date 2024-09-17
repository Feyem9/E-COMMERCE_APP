from flask import Flask , request , jsonify , session , redirect , url_for , current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager 
from flask_session import Session
from flask_migrate import Migrate
from flask_mail import Mail , Message
from flask_cors import CORS

from config import db, SECRET_KEY , MAIL_SERVER , MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD,MAIL_USE_SSL,MAIL_USE_TLS, MAIL_DEFAULT_SENDER

from models.customer_model import Customers

from routes.customer_route import cust_bp
from routes.cart_route import cart
# from routes.categoriy_route import category
# from routes.favorite_route import favorite
from routes.order_route import order
from routes.product_route import product
# from routes.transaction_route import transaction

db
app = Flask(__name__)
CORS(app)
app.config.from_object('config')
jwt = JWTManager(app)
app.secret_key = SECRET_KEY
app.MAIL_SERVER = MAIL_SERVER
app.MAIL_PORT = MAIL_PORT
app.MAIL_USERNAME = MAIL_USERNAME
app.MAIL_PASSWORD = MAIL_PASSWORD
app.MAIL_USE_SSL = MAIL_USE_SSL
app.MAIL_USE_TLS = MAIL_USE_TLS
app.MAIL_DEFAULT_SENDER = MAIL_DEFAULT_SENDER

mail = Mail(app)

# Configuration pour Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

bcrypt = Bcrypt(app)

# Configuration pour Flask-Login


from functools import wraps
from flask import jsonify, abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


# Configuration pour Flask-SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

def send_email(to, subject, template, **kwargs):
    with current_app.app_context():
        msg = Message(subject='hello good to se you', recipients=[to], html=template, sender=(current_app.config['MAIL_DEFAULT_SENDER'],'e_commerce_app'))
        mail.send(msg)

def show_image(value):
    print(len(value))

    if len(value) != 1:
        
        pics = value.split(' ')
        return pics[0].replace("'","")
    return ''

app.jinja_env.globals.update(show_image=show_image)


app.register_blueprint(cust_bp , url_prefix='/')
app.register_blueprint(cart , url_prefix='/cart')
# app.register_blueprint(category , url_prefix='/category')
# app.register_blueprint(favorite , url_prefix='/favorite')
app.register_blueprint(order , url_prefix='/order')
app.register_blueprint(product , url_prefix='/product')
# app.register_blueprint(transaction , url_prefix='/transaction')

# Gestion des erreurs 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Exemple de gestion d'erreurs 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

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

# payment = payUnit({
#     "apiUsername":'',
#     "apiPassword":'',
#     "api_key":'',
#     "return_url": "",
#     "notify_url":"",
#     "mode": "",
#     "name": "",
#     "description": "",
#     "purchaseRef": "",
#     "currency": "",
#    "transaction_id":  ""
# })
# payment.makePayment(5000)

# routes/mail_test.py
@app.route('/test-email')
def test_email():
    from flask import current_app
    from flask_mail import Message
    msg = Message(
        subject='Test Email',
        recipients=['feyemlionel@gmail.com'],  # Remplacez par votre email de test
        body='This is a test email.',
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    return 'Email sent!'


if __name__ == '__main__':
    app.run(debug=True)
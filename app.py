from flask import Flask , request , jsonify , session , redirect , url_for , current_app#type:ignore
from flask_bcrypt import Bcrypt#type:ignore
from flask_jwt_extended import JWTManager #type:ignore
from flask_session import Session
from flask_migrate import Migrate#type:ignore
from flask_mail import Mail , Message#type:ignore
from flask_cors import CORS#type:ignore

from config import db, SECRET_KEY , MAIL_SERVER , MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD,MAIL_USE_SSL,MAIL_USE_TLS, MAIL_DEFAULT_SENDER

from models.cart_model import Carts
from models.customer_model import Customers

from routes.customer_route import customer
from routes.cart_route import cart
from routes.order_route import order
from routes.product_route import product
from routes.transaction_route import transaction

# db
app = Flask(__name__)
CORS(app)

# Autoriser CORS pour toutes les routes
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True, methods=['GET', 'POST', 'OPTIONS' , 'DELETE' , 'PUT'], allow_headers=['Content-Type', 'Authorization'])


# Configuration de l'application pour l'envoie des mails
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
from flask import jsonify, abort#type:ignore
from flask_login import current_user#type:ignore

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



app.register_blueprint(customer , url_prefix='/customer')
app.register_blueprint(cart , url_prefix='/cart')
app.register_blueprint(order , url_prefix='/order')
app.register_blueprint(product , url_prefix='/product') 
app.register_blueprint(transaction , url_prefix='/transaction')

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
    from flask import current_app#type:ignore
    from flask_mail import Message#type:ignore
    msg = Message(
        subject='Test Email',
        recipients=['feyemlionel@gmail.com'],  # Remplacez par votre email de test
        body='This is a test email.',
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    return 'Email sent!'


@app.route('/update-cart/<id>' ,methods=['POST'])
def update_cart(id):
    if request.method != 'POST':
        return jsonify({'error': 'Méthode non autorisée'}), 405

    cart = Carts.query.filter_by(id=id).first()
    if not cart:
        return jsonify({'error': 'Produit introuvable dans le panier.'}), 404

    data = request.get_json()
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Données de quantité manquantes'}), 400

    try:
        quantity = int(data['quantity'])
        if quantity < 0:
            return jsonify({'error': 'La quantité doit être un nombre positif'}), 400
        
        cart.quantity = quantity
        db.session.commit()
        
        return jsonify({
            'message': 'Quantité mise à jour avec succès.',
            'new_quantity': cart.quantity
        }), 200
    except ValueError:
        return jsonify({'error': 'La quantité doit être un nombre valide'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
from flask import render_template, request, jsonify, current_app, url_for#type:ignore
from werkzeug.security import generate_password_hash##type:ignore
from itsdangerous import URLSafeTimedSerializer#type:ignore
    
    
@app.route('/check-session')
def check_session():
    return jsonify(dict(session))

from flask import abort, render_template , redirect , request , session , url_for , jsonify , Blueprint , abort
from werkzeug.security import generate_password_hash , check_password_hash 
from models.customer_model import Customers
from config import db
from itsdangerous import URLSafeTimedSerializer
from flask_login import  current_user
from flask_login import LoginManager
# from utility.mail import send_email
from flask_mail import Message , Mail
from flask import current_app

mail = Mail()

login_manager = LoginManager()
@login_manager.user_loader
def load_user(customer_id):
    return Customers.query.get(int(customer_id))



SECRET_KEY = '123'
s = URLSafeTimedSerializer(SECRET_KEY)

def send_email(to, subject, template, **kwargs):
    with current_app.app_context():
        msg = Message(subject='hello good to se you', recipients=[to], html=template, sender=(current_app.config['MAIL_DEFAULT_SENDER'],'e_commerce_app'))
        mail.send(msg)
def admin_required(f):
    @wraps(f) #type:ignore
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  
        return f(*args, **kwargs)
    return decorated_function


def home():
    return render_template('home.html')
def register():
    return render_template('/customers/register.html')

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    contact = request.form.get('contact')
    address = request.form.get('address')
    role = request.form.get('role')
    if not all([email, name, password, contact, address,role]):
        return redirect('/register?error=missing_data')
    
    print(email , address,role)
    customer = Customers.query.filter_by(email=email).first()
    if customer:
        return redirect('/register?error=email_exists')

    new_customer = Customers(email, name, generate_password_hash(password, salt_length=32), contact, address,role)
    db.session.add(new_customer)
    db.session.commit()

    token = s.dumps(email, salt='email-confirm')
    confirm_url = url_for('customer.confirm_email', token=token, _external=True)
    html = render_template('email/confirm_email.html', name=name, confirm_url=confirm_url)

    send_email(email, 'Confirmez votre inscription', html)

    return redirect('/login?please check your email')
    # return jsonify({'message': 'Customer registered successfully'}), 201
def login():
    return render_template('/customers/login.html')

def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    customer = Customers.query.filter_by(email=email).first()
    # if customer and check_password_hash(customer.password, password):
    if customer != customer :
        return redirect('/login?error=register_first' , message='please register before login')
    elif check_password_hash(customer.password , password) == False:
        return redirect('/login?error=incorrect_password')
    print(session)
    session['customer']={"id" :customer.id,
     "name" :customer.name,
     "email" :customer.email,
     "contact" :customer.contact,
     "address" :customer.address
    }
    return redirect('/')
    # return redirect('/')
def logout():
    if 'customer_id' in session:
        session.pop('customer_id', None)
    return redirect('/')

def profile():
    if 'customer' not in session:
        return redirect('/login')
    
    print(session.get('customer'))
    customer_id = session.get('customer')['id']
    print(customer_id['id'])
    customer = Customers.query.filter_by(id=customer_id).first()
 
    return render_template('/customers/profile.html', customer=customer)

def forgot_password():
    return render_template('/customers/forgot_password.html')

def forgot_password_post():
    # email = request.form.get('email')
    # customer = Customers.query.filter_by(email=email).first()
    # indexs = index
    # return indexs
    # if customer:
    #     token = s.dumps(email, salt='email-confirm')
    #     confirm_url = url_for('confirm_email', token=token, _external=True)
    #     html = render_template('activate.html', confirm_url=confirm_url)
    #     subject = "Please confirm your email"
    #     # send_email(customer.email, subject, html)
        # return redirect('/login')
    return redirect('/forgot-password')

# def new_func(confirm_url):
#     html = render_template('activate.html', confirm_url=confirm_url)


def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        abort(404)
    customer = Customers.query.filter_by(email=email).first_or_404()
    if customer.confirmed:
        return redirect(url_for('login'))
    customer.confirmed = True
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('customer.login'))

# def reset_password():
#     return render_template('reset_password.html')

# def reset_password_post():
#     email = request.form.get('email')
#     customer = Customers.query.filter_by(email=email).first()
#     if customer:
#         token = s.dumps(email, salt='email-confirm')
#         confirm_url = url_for('confirm_email', token=token, _external=True)
#         html = render_template('activate.html', confirm_url=confirm_url)
#         subject = "Please confirm your email"
#         send_email(customer.email, subject, html)
#         return redirect('/login')
#     return redirect('/reset_password')

# def reset_password_confirm(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except:
#         abort(404)
#     customer = Customers.query.filter_by(email=email).first_or_404()
#     if customer.confirmed:
#         return redirect(url_for('login'))
#     customer.confirmed = True
#     db.session.add(customer)
#     db.session.commit()
#     return redirect(url_for('login'))
#
from flask import abort, render_template , redirect , request , session , url_for 
from werkzeug.security import generate_password_hash , check_password_hash 
from models.customer_model import Customers
from config import db 
# ,mail , index
from itsdangerous import URLSafeTimedSerializer


# app.MAIL_SERVER = MAIL_SERVER
# app.MAIL_PORT = MAIL_PORT
# app.MAIL_USERNAME = MAIL_USERNAME
# app.MAIL_PASSWORD = MAIL_PASSWORD
# app.MAIL_USE_SSL = MAIL_USE_SSL
# app.MAIL_USE_TLS = MAIL_USE_TLS

# mails = mail

SECRET_KEY = '123'
s = URLSafeTimedSerializer(SECRET_KEY)

def home():
    return render_template('home.html')
def register():
    return render_template('/customers/register.html')

def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    contact = request.form.get('contact')
    address = request.form.get('address')
    print(email , address)
    customer = Customers.query.filter_by(email=email).first()
    if customer:
        return redirect('/customers/register')

    new_customer = Customers(email, name, generate_password_hash(password, salt_length=32), contact, address)
    db.session.add(new_customer)
    db.session.commit()
    return redirect('/customers/login')
def login():
    return render_template('/customers/login.html')

def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    customer = Customers.query.filter_by(email=email).first()
    # if customer and check_password_hash(customer.password, password):
    if customer != customer :
        return redirect('/login' , message='please register before login')
    elif check_password_hash(customer.password , password) == False:
        return redirect('/customers/login')
    # print(session)
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
        return redirect('/customers/login')
    
    # print(session.get('customer'))
    customer_id = session.get('customer')['id']
    # print(customer_id['id'])
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

def new_func(confirm_url):
    html = render_template('activate.html', confirm_url=confirm_url)


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
    return redirect(url_for('login'))

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
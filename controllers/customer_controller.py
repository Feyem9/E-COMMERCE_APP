from flask import abort,app, render_template , redirect , request , session , url_for 
from werkzeug.security import generate_password_hash , check_password_hash 
from models.customer_model import Customers
from config import db
from itsdangerous import URLSafeTimedSerializer
# from utils import send_email #type:ignore
# import os

# app.config['SECRET_KEY'] = os.urandom(24)#type:ignore
# s = URLSafeTimedSerializer(app.config['SECRET_KEY'])#type:ignore
def register():
    return render_template('register.html')

def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    contact = request.form.get('contact')
    address = request.form.get('address')
    customer = Customers(email, name, generate_password_hash(password), contact, address)
    db.session.add(customer)
    db.session.commit()
    return redirect('/login')
def login():
    return render_template('login.html')

def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    customer = Customers.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        session['customer_id'] = customer.id
        return redirect('/')
    return redirect('/login')

def logout():
    if 'customer_id' in session:
        session.pop('customer_id', None)
    return redirect('/')

def profile():
    if 'customer_id' not in session:
        return redirect('/login')
    customer_id = session.get('customer_id')
    customer = Customers.query.filter_by(id=customer_id).first()
    return render_template('profile.html', customer=customer)

def forgot_password():
    return render_template('forgot_password.html')

def forgot_password_post():
    email = request.form.get('email')
    customer = Customers.query.filter_by(email=email).first()
    if customer:
        token = s.dumps(email, salt='email-confirm')#type:ignore
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(customer.email, subject, html)#type:ignore
        return redirect('/login')
    return redirect('/forgot_password')


def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)#type:ignore
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
from flask import render_template , request  , redirect , url_for
from config import db
from models.cart_model import Carts

def index():
    carts = Carts.query.all()
    return render_template('/carts/index_cart.html', carts=carts)

# def view_cart(id):
#     cart = Carts.query.filter_by(id=id).first()
#     if not cart:
#         return redirect(url_for('index_cart'))
#     return render_template('view_cart.html', cart=cart)

def update_cart(id):
    cart = Carts.query.filter_by(id=id).first()
    if not cart:
        return redirect(url_for('index_cart'))
    if request.method == 'GET':
        return render_template('update_cart.html', cart=cart)
    elif request.method == 'POST':
        quantity = request.form.get('quantity')
        cart.quantity = quantity
        db.session.add(cart)
        db.session.commit()
        return redirect(url_for('index_cart'))  
    return render_template('update_cart.html', cart=cart , title='Update Cart successfully')

def delete_cart(id):
    if request.method == 'POST':
        if request.form.get('delete'):
            cart = Carts.query.filter_by(id=id).first()
            db.session.delete(cart)
            db.session.commit()
            return redirect(url_for('index_cart'))


from flask import render_template , request  , redirect , url_for , session ,send_from_directory
from config import db , UPLOAD_EXTENSIONS , UPLOAD_PATH
import os
import imghdr
import uuid
from werkzeug.utils import secure_filename

# from models.cart_model import Carts
from models.product_model import Products



# def validate_image(stream):
#     header = stream.read(512)
#     stream.seek(0)
#     format = imghdr.what(None, header)
#     if not format:
#         return None
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else ".jpeg") if format != "avif" else ".avif" if format != "png" else ".png"


def index_product():
    products = Products.query.all()
    return render_template('/products/index_product.html', products=products , title="products")

def add_product():
    return render_template('/products/add_product.html' , title='Add Product')

def create():
  
    name = request.form.get('name')
    description = request.form.get('description')
    current_price = request.form.get('current_price')
    discount_price = request.form.get('discount_price')
    quantity = request.form.get('quantity')
  
    picture = request.files.get('picture')
    if picture is None:
        return {"error": "No picture uploaded"}, 400

    
    filename = secure_filename(picture.filename)
    if filename:
        file_ext = os.path.splitext(filename)[
            1]
        
        if file_ext not in UPLOAD_EXTENSIONS:
            print(file_ext)
        
            return {"error": "File type not supported"}, 400
        
        existing_product = Products.query.filter_by(picture=filename).first()
        if existing_product:
            unique_str = str(uuid.uuid4())[:8]
            filename = f"{unique_str}_{filename}"

        picture.save(os.path.join(UPLOAD_PATH, filename))

    product = Products(name, description, current_price, discount_price, quantity, picture)
    print(picture)
    db.session.add(product)
    db.session.commit()

    return redirect('/product')

def view_product(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return redirect(url_for('index_product'))
    return render_template('/products/view_product.html', product=product)

def update_product(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return redirect(url_for('product.index_product'))
    if request.method == 'GET':
        return render_template('/products/update_product.html', product=product)
    elif request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        current_price = request.form.get('current_price')
        discount_price = request.form.get('discount_price')
        quantity = request.form.get('quantity')
        picture = request.files.get('picture')
        product.name = name
        product.description = description
        product.current_price = current_price
        product.discount_price = discount_price
        product.quantity = quantity
        product.picture = picture
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product.index_product'))  
    return render_template('/products/update_product.html', product=product , title='Update Product successfully')  

def delete_product(id):
    if request.method == 'POST':
        if request.form['_method'] == 'DELETE':
            product = Products.query.get(id)
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for('product.index_product'))


def search():
    if request.method == 'GET':
        return render_template('search.html')
    elif request.method == 'POST':
        search = request.form.get('search')
        products = Products.query.filter(Products.name.like('%'+search+'%')).all()
        return render_template('search.html', products=products)
    

def search_product(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return redirect(url_for('index_product'))
    return render_template('search_product.html', product=product)

def add_to_cart(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return redirect(url_for('index_product'))
    return render_template('/carts/index_cart.html', product=product)

def add_to_cart_post(id):
    product = Products.query.filter_by(id=id).first()
    if not product:
        return redirect(url_for('index_product'))
    quantity = request.form.get('quantity')
    customer_id = request.form.get('customer_id')
    cart = Carts(quantity, customer_id, product_id) # type: ignore
    db.session.add(cart)
    db.session.commit()
    return render_template('/carts/index_cart.html')

# def view_cart():
#     if 'customer_id' not in session:
#         return redirect('/login')
#     customer_id = session.get('customer_id')
#     carts = Carts.query.filter_by(customer_id=customer_id).all()
#     return render_template('view_cart.html', carts=carts)

# def delete_cart(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             cart = Carts.query.filter_by(id=id).first()
#             db.session.delete(cart)
#             db.session.commit()
#             return redirect(url_for('view_cart'))
        
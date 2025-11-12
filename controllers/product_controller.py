from flask import jsonify, render_template , request  , redirect , url_for , session ,send_from_directory
from config import db , UPLOAD_EXTENSIONS , UPLOAD_PATH
import os
import imghdr
import uuid
from werkzeug.utils import secure_filename
import cloudinary.uploader

from models.cart_model import Carts
from models.product_model import Products
from flask_jwt_extended import jwt_required, get_jwt_identity




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
    return "." + (format if format != "jpeg" else ".jpeg") if format != "avif" else ".avif" if format != "png" else ".png" if format != "webp" else ".webp"


def index_product():
    products = Products.query.all()
    products_list = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "current_price": product.current_price,
        "discount_price": product.discount_price,
        "quantity": product.quantity,
        "picture": product.picture
    } for product in products]
    return jsonify(products_list), 200

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
        return jsonify({"error": "no picture uploaded"}), 400

    filename = secure_filename(picture.filename)
    if filename:
        file_ext = os.path.splitext(filename)[1]

        if file_ext not in UPLOAD_EXTENSIONS:
            return jsonify({"error": "File type not supported"}), 400

        # Upload to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(picture, folder="ecommerce_products")
            picture_url = upload_result['secure_url']
        except Exception as e:
            return jsonify({"error": f"Upload failed: {str(e)}"}), 500

    product = Products(name=name, description=description, current_price=current_price, discount_price=discount_price, quantity=quantity, picture=picture_url)
    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id" : product.id,
        "name" : product.name,
        "description": product.description,
        "current_price": product.current_price,
        "discount_price": product.discount_price,
        "quantity": product.quantity,
        "picture": product.picture
    }),200

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
    quantity = request.form.get('quantity')
    customer_id = request.form.get('customer_id')
    print(product.id)
    cart = Carts(int(quantity), customer_id, id) 
    print(cart)
    print("Données reçues :", request.get_json())
    db.session.add(cart)
    db.session.commit()
    return jsonify({
        "message": "Produit ajouté au panier",
        "status":"success",
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "current_price": product.current_price,
        }}), 200
    
    return render_template('/carts/index_cart.html', product=product)

@jwt_required()
def add_to_cart_post(id):
    # customer_id = get_jwt_identity()  # extrait depuis le token
    # print("customer_id :", customer_id)
    # if not customer_id:
    #     return jsonify({'error': "L'ID du client est requis"}), 400
    product = Products.query.filter_by(id=id).first()
    if not product:
        return jsonify({"error": "Produit introuvable"}), 404

    # Récupération des données JSON de la requête
    data = request.get_json()
    print("Données reçues :", data)

    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    quantity = data.get('quantity')
    customer_id = data.get('customer_id')
    print(quantity)

    # Validation des données
    if not quantity:
        return jsonify({"error": "La quantité est requise"}), 400
    if not customer_id:
        return jsonify({"error": "L'ID du client est requis"}), 400

    try:
        product_name = product.name if product else None
        if not product_name:
            return jsonify({"error": "Le nom du produit est introuvable"}), 400
        print(product_name)
        cart = Carts(quantity=int(quantity),product_id=product.id , product_name=product.name , product_description=product.description , product_image=product.picture, current_price=product.current_price , customer_id=customer_id)
        print(cart)
        db.session.add(cart)
        db.session.commit()

        return jsonify({
            "message": "Produit ajouté au panier",
            "status": "success",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "current_price": product.current_price,
                "picture":product.picture,
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


        
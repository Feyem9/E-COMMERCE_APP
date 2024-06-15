# from flask import render_template , request  , redirect , url_for , session
# from config import db
# from models.cart_model import Carts
# from models.product_model import Products


# def index():
#     products = Products.query.all()
#     return render_template('index_product.html', products=products)

# def add_product():
#     return render_template('add_product.html' , title='Add Product')

# def create():
#     name = request.form.get('name')
#     description = request.form.get('description')
#     current_price = request.form.get('current_price')
#     discount_price = request.form.get('discount_price')
#     quantity = request.form.get('quantity')
#     picture = request.form.get('picture')
#     flash_sale = request.form.get('flash_sale')
#     product = Products(name, description, current_price, discount_price, quantity, picture, flash_sale)
#     db.session.add(product)
#     db.session.commit()
#     return redirect(url_for('index_product'))

# def view_product(id):
#     product = Products.query.filter_by(id=id).first()
#     if not product:
#         return redirect(url_for('index_product'))
#     return render_template('view_product.html', product=product)

# def update_product(id):
#     product = Products.query.filter_by(id=id).first()
#     if not product:
#         return redirect(url_for('index_product'))
#     if request.method == 'GET':
#         return render_template('update_product.html', product=product)
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         description = request.form.get('description')
#         current_price = request.form.get('current_price')
#         discount_price = request.form.get('discount_price')
#         quantity = request.form.get('quantity')
#         picture = request.form.get('picture')
#         flash_sale = request.form.get('flash_sale')
#         product.name = name
#         product.description = description
#         product.current_price = current_price
#         product.discount_price = discount_price
#         product.quantity = quantity
#         product.picture = picture
#         product.flash_sale = flash_sale
#         db.session.add(product)
#         db.session.commit()
#         return redirect(url_for('index_product'))  
#     return render_template('update_product.html', product=product , title='Update Product successfully')  

# def delete_product(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             product = Products.query.filter_by(id=id).first()
#             db.session.delete(product)
#             db.session.commit()
#             return redirect(url_for('index_product'))
        

# def search():
#     if request.method == 'GET':
#         return render_template('search.html')
#     elif request.method == 'POST':
#         search = request.form.get('search')
#         products = Products.query.filter(Products.name.like('%'+search+'%')).all()
#         return render_template('search.html', products=products)
    

# def search_product(id):
#     product = Products.query.filter_by(id=id).first()
#     if not product:
#         return redirect(url_for('index_product'))
#     return render_template('search_product.html', product=product)

# def add_to_cart(id):
#     product = Products.query.filter_by(id=id).first()
#     if not product:
#         return redirect(url_for('index_product'))
#     return render_template('add_to_cart.html', product=product)

# def add_to_cart_post(id):
#     product = Products.query.filter_by(id=id).first()
#     if not product:
#         return redirect(url_for('index_product'))
#     quantity = request.form.get('quantity')
#     customer_id = request.form.get('customer_id')
#     cart = Carts(quantity, customer_id, product_id) # type: ignore
#     db.session.add(cart)
#     db.session.commit()
#     return redirect(url_for('index_product'))

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
        
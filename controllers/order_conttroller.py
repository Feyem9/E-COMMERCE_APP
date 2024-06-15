# from flask import render_template , request  , redirect , url_for , session
# from config import db
# from models.cart_model import Carts
# from models.order_model import Orders

# def index():
#     orders = Orders.query.all()
#     return render_template('index_order.html', orders=orders)

# def view_order(id):
#     order = Orders.query.filter_by(id=id).first()
#     if not order:
#         return redirect(url_for('index_order'))
#     return render_template('view_order.html', order=order)

# def update_order(id):
#     order = Orders.query.filter_by(id=id).first()
#     if not order:
#         return redirect(url_for('index_order'))
#     if request.method == 'GET':
#         return render_template('update_order.html', order=order)
#     elif request.method == 'POST':
#         status = request.form.get('status')
#         order.status = status
#         db.session.add(order)
#         db.session.commit()
#         return redirect(url_for('index_order'))  
#     return render_template('update_order.html', order=order , title='Update Order successfully')

# def delete_order(id):
#     if request.method == 'POST':
#         if request.form.get('delete'):
#             order = Orders.query.filter_by(id=id).first()
#             db.session.delete(order)
#             db.session.commit()
#             return redirect(url_for('index_order'))

# def place_order(id):
#     order = Orders.query.filter_by(id=id).first()
#     if not order:
#         return redirect(url_for('index_order'))
#     return render_template('place_order.html', order=order)

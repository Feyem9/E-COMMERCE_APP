from flask import Blueprint #type:ignore

from controllers.cart_controller import index ,update_cart, delete_cart

cart = Blueprint('cart', __name__)

cart.route('/', methods=['GET'])(index)
cart.route('/update-cart/<id>', methods=['PUT'])(update_cart)
cart.route('/delete-cart/<id>', methods=['DELETE'])(delete_cart)
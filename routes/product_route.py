from flask import Blueprint

from controllers.product_controller import index_product , add_product , create , view_product , update_product , delete_product , search , search_product , add_to_cart , add_to_cart_post 
# , view_cart , delete_cart

product = Blueprint('product', __name__)

product.route('/', methods=['GET'])(index_product)
product.route('/add-product', methods=['GET'])(add_product)
product.route('/create', methods=['POST'])(create)
product.route('/view-product/<id>', methods=['GET'])(view_product)
product.route('/update-product/<id>', methods=['GET', 'POST'])(update_product)
product.route('/delete-product/<id>', methods=['POST'])(delete_product)
product.route('/search', methods=['GET', 'POST'])(search)
product.route('/search_product/<id>', methods=['GET'])(search_product)
product.route('/add-to-cart/<id>', methods=['GET', 'POST'])(add_to_cart)
product.route('/add-to-cart-post/<id>', methods=['POST'])(add_to_cart_post)
# product.route('/view_cart')(view_cart)
# product.route('/delete_cart/<id>', methods=['POST'])(delete_cart)

# from flask import Blueprint

# from controllers.product_controller import index , add_product , create , view_product , update_product , delete_product , search , search_product , add_to_cart , add_to_cart_post , view_cart , delete_cart

# product = Blueprint('product', __name__)

# product.route('/', methods=['GET'])(index)
# product.route('/add_product', methods=['GET', 'POST'])(add_product)
# product.route('/create', methods=['GET', 'POST'])(create)
# product.route('/view_product/<id>', methods=['GET'])(view_product)
# product.route('/update_product/<id>', methods=['GET', 'POST'])(update_product)
# product.route('/delete_product/<id>', methods=['POST'])(delete_product)
# product.route('/search', methods=['GET', 'POST'])(search)
# product.route('/search_product/<id>', methods=['GET'])(search_product)
# product.route('/add_to_cart/<id>', methods=['GET', 'POST'])(add_to_cart)
# product.route('/add_to_cart_post/<id>', methods=['POST'])(add_to_cart_post)
# product.route('/view_cart')(view_cart)
# product.route('/delete_cart/<id>', methods=['POST'])(delete_cart)

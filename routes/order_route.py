from flask import Blueprint

from controllers.order_controller import index ,view_order , update_order , place_order , delete_order 

order = Blueprint('order', __name__)

order.route('/', methods=['GET'])(index)
order.route('/view_order/<id>', methods=['GET'])(view_order)
order.route('/update_order/<id>', methods=['GET' , 'POST'])(update_order)
order.route('/place_order/<id>', methods=['GET'])(place_order)
order.route('/delete_order/<id>', methods=['POST'])(delete_order)
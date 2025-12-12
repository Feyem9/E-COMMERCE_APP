from flask import Blueprint #type:ignore

from controllers.category_controller import index, show_category_form, add_category, view_category, update_category, delete_category

category = Blueprint('category', __name__)

category.route('/', methods=['GET'])(index)
category.route('/category', methods=['GET', 'POST'])(show_category_form)
category.route('/add_category', methods=['GET', 'POST'])(add_category)
category.route('/view_category/<id>', methods=['GET'])(view_category)
category.route('/update_category/<id>', methods=['GET', 'POST'])(update_category)
category.route('/delete_category/<id>', methods=['POST'])(delete_category)

from flask import Blueprint #type: ignore

from controllers.customer_controller import register, login, check_session , logout, profile, forgot_password, confirm_email, reset_password,all_users, register_options

customer = Blueprint('customer', __name__)

customer.route('/check-session', methods=['GET'] )(check_session)
customer.route('/customer', methods=['GET'])(all_users)
customer.route('/register', methods=['POST', 'OPTIONS'])(register)
customer.route('/register', methods=['OPTIONS'])(register_options)
customer.route('/login', methods=['POST'])(login)
customer.route('/logout')(logout)
customer.route('/profile' , methods=['GET'] ,strict_slashes=False)(profile)
customer.route('/forgot-password', methods=['GET', 'POST'])(forgot_password)

customer.route('/reset-password/<token>' , methods=['GET', 'POST'])(reset_password)
customer.route('/confirm-email/<token>')(confirm_email)

customer.route('/admin/users')(all_users)
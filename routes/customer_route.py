from flask import Blueprint

from controllers.customer_controller import home,register, register_post, login, login_post, logout, profile, forgot_password, forgot_password_post, confirm_email

customer = Blueprint('customer', __name__)

customer.route('/' )(home)
customer.route('/register', methods=['GET', 'POST'])(register)
customer.route('/register-post', methods=['POST'])(register_post)
customer.route('/login', methods=['GET'])(login)
customer.route('/login-post', methods=['POST'])(login_post)
customer.route('/logout')(logout)
customer.route('/profile' , methods=['GET'] ,strict_slashes=False)(profile)
customer.route('/forgot-password', methods=['GET'])(forgot_password)
customer.route('/forgot-password-post', methods=['POST'])(forgot_password_post)
customer.route('/confirm-email/<token>')(confirm_email)
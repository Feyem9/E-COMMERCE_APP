from flask import Blueprint

from controllers.customer_controller import register, register_post, login, login_post, logout, profile, forgot_password, forgot_password_post, confirm_email

customer = Blueprint('customer', __name__)

customer.route('/register', methods=['GET', 'POST'])(register)
customer.route('/register-post', methods=['POST'])(register_post)
customer.route('/login', methods=['GET', 'POST'])(login)
customer.route('/login-post', methods=['POST'])(login_post)
customer.route('/logout')(logout)
customer.route('/profile')(profile)
customer.route('/forgot_password', methods=['GET', 'POST'])(forgot_password)
customer.route('/forgot_password-post', methods=['POST'])(forgot_password_post)
customer.route('/confirm_email/<token>')(confirm_email)
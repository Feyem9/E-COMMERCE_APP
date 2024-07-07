from flask import Blueprint

from controllers.customer_controller import home,register, register_post, login, login_post, logout, profile, forgot_password, forgot_password_post, confirm_email

cust_bp = Blueprint('customer', __name__)

cust_bp.route('/' )(home)
cust_bp.route('/register', methods=['GET'])(register)
cust_bp.route('/register-post', methods=['POST'])(register_post)
cust_bp.route('/login', methods=['GET'])(login)
cust_bp.route('/login-post', methods=['POST'])(login_post)
cust_bp.route('/logout')(logout)
cust_bp.route('/profile' , methods=['GET'] ,strict_slashes=False)(profile)
cust_bp.route('/forgot-password', methods=['GET'])(forgot_password)
cust_bp.route('/forgot-password-post', methods=['POST'])(forgot_password_post)
cust_bp.route('/confirm-email/<token>')(confirm_email)
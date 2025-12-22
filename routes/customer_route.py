from flask import Blueprint #type: ignore

from controllers.customer_controller import register, login, check_session , logout, profile, forgot_password, confirm_email, reset_password,all_users, register_options

customer = Blueprint('customer', __name__)

# Import Rate Limiter from extensions
from extensions import limiter

# Routes standards
customer.route('/check-session', methods=['GET'] )(check_session)
customer.route('/customer', methods=['GET'])(all_users)

# ============================================
# ROUTES PROTÉGÉES PAR RATE LIMITING
# ============================================

# REGISTER : 3 tentatives par heure (protection spam)
customer.route('/register', methods=['POST', 'OPTIONS'])(
    limiter.limit("3 per hour")(register)
)
customer.route('/register', methods=['OPTIONS'])(register_options)

# LOGIN : 5 tentatives par minute (protection brute force)
customer.route('/login', methods=['POST'])(
    limiter.limit("5 per minute")(login)
)

customer.route('/logout')(logout)
customer.route('/profile' , methods=['GET'] ,strict_slashes=False)(profile)

# FORGOT PASSWORD : 3 tentatives par heure (protection email bombing)
customer.route('/forgot-password', methods=['GET', 'POST'])(
    limiter.limit("3 per hour")(forgot_password)
)

customer.route('/reset-password/<token>' , methods=['GET', 'POST'])(reset_password)
customer.route('/confirm-email/<token>')(confirm_email)

customer.route('/admin/users')(all_users)
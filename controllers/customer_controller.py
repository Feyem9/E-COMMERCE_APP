from flask import Blueprint, render_template, redirect, request, session, url_for, jsonify, abort#type:ignore
from werkzeug.security import generate_password_hash, check_password_hash#type:ignore
from models.customer_model import Customers
from config import db
from itsdangerous import URLSafeTimedSerializer#type:ignore
from flask_login import LoginManager, login_user, logout_user, login_required, current_user#type:ignore
from flask_mail import Message, Mail#type:ignore
from flask import current_app#type:ignore
from functools import wraps
from flask_jwt_extended import create_access_token , jwt_required, get_jwt_identity , decode_token#type:ignore


customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

mail = Mail()
login_manager = LoginManager()
s = URLSafeTimedSerializer('your-secret-key')  # Remplacez par une clé secrète sécurisée

@login_manager.user_loader
def load_user(customer_id):
    return Customers.query.get(int(customer_id))

def send_email(to, subject, template):

    with current_app.app_context():
         msg = Message(subject='hello good to se you', recipients=[to], html=template, sender=(current_app.config['MAIL_DEFAULT_SENDER'],'e_commerce_app'))
         mail.send(msg)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

#
def register():
    try:
        if request.method == 'POST':
            # Assurez-vous que les données sont bien en JSON
            if not request.is_json:
                current_app.logger.error("Content-Type n'est pas JSON")
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            if not data:
                current_app.logger.error("Pas de données JSON reçues")
                return jsonify({'error': 'Pas de données reçues'}), 400

            email = data.get('email', '').strip().lower()
            name = data.get('name', '').strip()
            password = data.get('password', '')
            contact = data.get('contact', '').strip()
            address = data.get('address', '').strip()
            role = data.get('role', 'user')

            current_app.logger.info(f"Données reçues : email={email}, name={name}, contact={contact}, address={address}, role={role}")

            # Vérification des champs requis
            missing = [field for field in ['email', 'name', 'password', 'contact', 'address'] if not data.get(field)]
            if missing:
                current_app.logger.error(f"Données manquantes : {', '.join(missing)}")
                return jsonify({'error': 'Données manquantes pour l\'inscription'}), 400

            # Vérification de l'unicité de l'email
            existing_user = Customers.query.filter_by(email=email).first()
            if existing_user:
                current_app.logger.error(f"Email déjà existant : {email}")
                return jsonify({'error': 'Cet email existe déjà'}), 400

            # Création du nouvel utilisateur
            new_customer = Customers(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                contact=contact,
                address=address,
                role=role
            )
            db.session.add(new_customer)
            db.session.commit()
            current_app.logger.info(f"Utilisateur créé avec succès : {email}")

            # Envoi de l'email de confirmation (optionnel - ne pas bloquer si erreur)
            try:
                s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                token = s.dumps(email, salt='email-confirm')
                confirm_url = url_for('customer.confirm_email', token=token, _external=True)
                html = render_template('email/confirm_email.html', name=name, confirm_url=confirm_url)
                send_email(email, 'Confirmez votre inscription', html)
                current_app.logger.info(f"Email de confirmation envoyé à : {email}")
            except Exception as e:
                current_app.logger.warning(f"Erreur lors de l'envoi d'email à {email} : {str(e)}")

            return jsonify({'message': 'Inscription réussie. Veuillez vérifier votre email.'}), 201

        # Pour les autres méthodes, retourner une erreur
        return jsonify({'error': 'Méthode non autorisée'}), 405

    except Exception as e:
        db.session.rollback()
        error_msg = f"Erreur lors de l'enregistrement : {str(e)}"
        current_app.logger.error(error_msg, exc_info=True)
        return jsonify({'error': 'Erreur lors de l\'enregistrement', 'details': str(e)}), 500



def login():
    data = request.get_json()

    email = data.get('email', '').lower()
    password = data.get('password')

    print("📩 Email:", email)
    print("🔒 Password:", password)

    customer = Customers.query.filter_by(email=email).first()

    if not customer:
        print("❌ Utilisateur non trouvé")
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

    if not check_password_hash(customer.password, password):
        print("❌ Mot de passe incorrect")
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

    # ✅ Authentification réussie
    token = create_access_token(identity=customer.id)
    decoded = decode_token(token)
    print('Token décodé:', decoded)
    
    
    # Date d'expiration en timestamp UNIX
    exp_timestamp = decoded['exp']
    print('Expiration timestamp:', exp_timestamp)
    login_user(customer)  # si tu utilises flask-login

    print("🎉 Connexion réussie pour :", customer.email)

    return jsonify({
        'access_token': token,
        'user': {
            'id': customer.id,
            'email': customer.email,
            'name': customer.name,
            'role': customer.role
        }
    }), 200



def check_session():
    return jsonify(dict(session))


# @customer_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        customer = Customers.query.filter_by(email=email).first()
        if customer:
            token = s.dumps(email, salt='password-reset')
            reset_url = url_for('customer.reset_password', token=token, _external=True)
            html = render_template('email/reset_password.html', reset_url=reset_url)
            send_email(email, 'Réinitialisation de mot de passe', html)
            return jsonify({'message': 'Instructions envoyées par email'}), 200
        return jsonify({'error': 'Email non trouvé'}), 404

    return render_template('/customers/forgot_password.html')

# @customer_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except:
        return jsonify({'error': 'Le lien est invalide ou a expiré'}), 400

    if request.method == 'POST':
        customer = Customers.query.filter_by(email=email).first()
        if customer:
            new_password = request.form.get('password')
            customer.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            return jsonify({'message': 'Mot de passe réinitialisé avec succès'}), 200
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    return render_template('/customers/reset_password.html', token=token)

# @customer_bp.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return jsonify({'error': 'Le lien de confirmation est invalide ou a expiré'}), 400

    customer = Customers.query.filter_by(email=email).first()
    if customer:
        if not customer.confirmed:
            customer.confirmed = True
            db.session.commit()
            return jsonify({'message': 'Email confirmé avec succès'}), 200
        return jsonify({'message': 'Email déjà confirmé'}), 200
    return jsonify({'error': 'Utilisateur non trouvé'}), 404


def all_users():
    customers = Customers.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200


@jwt_required()
def profile():
    try:
        customer_id = get_jwt_identity()  # récupère l'identité du token
        customer = Customers.query.filter_by(id=customer_id).first()

        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'contact': customer.contact,
            'address': customer.address,
            'role': customer.role
        }

        return jsonify(customer_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# def forgot_password():
#     return render_template('/customers/forgot_password.html')

# def forgot_password_post():
#     # email = request.form.get('email')
#     # customer = Customers.query.filter_by(email=email).first()
#     # indexs = index
#     # return indexs
#     # if customer:
#     #     token = s.dumps(email, salt='email-confirm')
#     #     confirm_url = url_for('confirm_email', token=token, _external=True)
#     #     html = render_template('activate.html', confirm_url=confirm_url)
#     #     subject = "Please confirm your email"
#     #     # send_email(customer.email, subject, html)
#         # return redirect('/login')
#     return redirect('/forgot-password')

# # def new_func(confirm_url):
# #     html = render_template('activate.html', confirm_url=confirm_url)


# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except:
#         abort(404)
#     customer = Customers.query.filter_by(email=email).first_or_404()
#     if customer.confirmed:
#         return redirect(url_for('login'))
#     customer.confirmed = True
#     db.session.add(customer)
#     db.session.commit()
#     return redirect(url_for('customer.login'))

# # def reset_password():
# #     return render_template('reset_password.html')

# # def reset_password_post():
# #     email = request.form.get('email')
# #     customer = Customers.query.filter_by(email=email).first()
# #     if customer:
# #         token = s.dumps(email, salt='email-confirm')
# #         confirm_url = url_for('confirm_email', token=token, _external=True)
# #         html = render_template('activate.html', confirm_url=confirm_url)
# #         subject = "Please confirm your email"
# #         send_email(customer.email, subject, html)
# #         return redirect('/login')
# #     return redirect('/reset_password')

# # def reset_password_confirm(token):
# #     try:
# #         email = s.loads(token, salt='email-confirm', max_age=3600)
# #     except:
# #         abort(404)
# #     customer = Customers.query.filter_by(email=email).first_or_404()
# #     if customer.confirmed:
# #         return redirect(url_for('login'))
# #     customer.confirmed = True
# #     db.session.add(customer)
# #     db.session.commit()
# #     return redirect(url_for('login'))
# #

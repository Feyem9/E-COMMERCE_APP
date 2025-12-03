from flask import Blueprint, render_template, redirect, request, session, url_for, jsonify, abort, current_app#type:ignore
from werkzeug.security import generate_password_hash, check_password_hash#type:ignore
from models.customer_model import Customers
from config import db
from itsdangerous import URLSafeTimedSerializer#type:ignore
from flask_login import LoginManager, login_user, logout_user, login_required, current_user#type:ignore
from flask_mail import Message#type:ignore
from functools import wraps
from flask_jwt_extended import create_access_token , jwt_required, get_jwt_identity , decode_token#type:ignore


customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

login_manager = LoginManager()
s = URLSafeTimedSerializer('your-secret-key')  # Remplacez par une clé secrète sécurisée

@login_manager.user_loader
def load_user(customer_id):
    return Customers.query.get(int(customer_id))

def send_email(to, subject, template):
    """Envoyer un email en utilisant la configuration Flask-Mail de l'app"""
    try:
        from flask_mail import Mail
        mail_instance = current_app.extensions.get('mail')
        if not mail_instance:
            current_app.logger.warning("Flask-Mail not initialized in app.extensions")
            return
        
        msg = Message(
            subject=subject, 
            recipients=[to], 
            html=template, 
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@ecommerce.com')
        )
        mail_instance.send(msg)
        current_app.logger.info(f"✅ Email sent to {to}")
    except Exception as e:
        current_app.logger.warning(f"⚠️ Error sending email to {to}: {str(e)}")

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
        if request.method != 'POST':
            return jsonify({'error': 'Method not allowed. Use POST.'}), 405

        # Vérifier le Content-Type
        if not request.is_json:
            try:
                current_app.logger.error(f"Invalid Content-Type: {request.content_type}")
            except:
                pass
            return jsonify({
                'error': 'Content-Type must be application/json',
                'details': f'Received Content-Type: {request.content_type}',
                'required': 'application/json'
            }), 400

        data = request.get_json()
        if data is None:
            try:
                current_app.logger.error("get_json() returned None")
            except:
                pass
            return jsonify({
                'error': 'Invalid JSON data',
                'details': 'Request body could not be parsed as JSON',
                'received_data': str(request.data)
            }), 400

        # Extraire les données avec des valeurs par défaut
        email = (data.get('email') or '').strip().lower()
        name = (data.get('name') or '').strip()
        password = data.get('password') or ''
        contact = (data.get('contact') or '').strip()
        address = (data.get('address') or '').strip()
        role = (data.get('role') or 'user').strip().lower()

        try:
            current_app.logger.info(f"Register attempt: email={email}, name={name}, role={role}")
        except:
            pass

        # Valider les champs requis
        if not email or not name or not password or not contact or not address:
            missing_fields = []
            if not email: missing_fields.append('email')
            if not name: missing_fields.append('name')
            if not password: missing_fields.append('password')
            if not contact: missing_fields.append('contact')
            if not address: missing_fields.append('address')

            try:
                current_app.logger.warning(f"Missing fields: {missing_fields}")
            except:
                pass
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'missing_fields': missing_fields,
                'received_data': {
                    'email': email,
                    'name': name,
                    'password': '*****' if password else '',
                    'contact': contact,
                    'address': address,
                    'role': role
                }
            }), 400

        # Valider le format de l'email
        if '@' not in email or '.' not in email:
            return jsonify({
                'error': 'Invalid email format',
                'details': 'Email must contain @ and . characters',
                'received_email': email
            }), 400

        # Valider la longueur du mot de passe
        if len(password) < 6:
            return jsonify({
                'error': 'Password too short',
                'details': 'Password must be at least 6 characters long',
                'received_length': len(password)
            }), 400

        # Vérifier que l'email n'existe pas déjà
        existing = Customers.query.filter(Customers.email == email).first()
        if existing:
            try:
                current_app.logger.warning(f"Email already exists: {email}")
            except:
                pass
            return jsonify({
                'error': 'Email already registered',
                'details': 'This email address is already in use',
                'existing_email': email
            }), 400

        # Hasher le mot de passe
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Créer le nouvel utilisateur
        new_customer = Customers(
            email=email,
            name=name,
            password=hashed_pw,
            contact=contact,
            address=address,
            role=role
        )
        
        # Sauvegarder dans la base de données
        db.session.add(new_customer)
        db.session.commit()
        current_app.logger.info(f"✅ Customer created successfully: {email}")

        # Essayer d'envoyer un email de confirmation (optionnel)
        try:
            s = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY', 'default-secret'))
            token = s.dumps(email, salt='email-confirm')
            confirm_url = url_for('customer.confirm_email', token=token, _external=True)
            
            # Ne pas utiliser render_template ici, créer le HTML directement
            html = f"""
            <html>
                <body>
                    <h2>Confirmez votre inscription</h2>
                    <p>Cliquez sur le lien ci-dessous pour confirmer votre email:</p>
                    <a href="{confirm_url}">Confirmer mon email</a>
                </body>
            </html>
            """
            
            send_email(email, 'Confirmez votre inscription', html)
            current_app.logger.info(f"Confirmation email sent to: {email}")
        except Exception as e:
            current_app.logger.warning(f"Could not send confirmation email to {email}: {str(e)}")
            # Ne pas échouer l'inscription si l'email échoue

        return jsonify({
            'message': 'Registration successful',
            'email': email,
            'name': name
        }), 201

    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        try:
            current_app.logger.error(f"Registration error: {error_msg}", exc_info=True)
        except:
            pass
        return jsonify({'error': 'Registration failed', 'details': error_msg}), 500

# Handle OPTIONS request for CORS preflight
def register_options():
    return jsonify({'message': 'CORS preflight successful'}), 200



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

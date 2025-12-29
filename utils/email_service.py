"""
📧 Service d'emails transactionnels
Templates HTML professionnels pour l'application e-commerce
"""

from flask import current_app, url_for
from flask_mail import Message
from datetime import datetime
import os

# Import conditionnel de mail
try:
    from app import mail
except ImportError:
    mail = None


def send_email(to, subject, html_content):
    """
    Envoie un email avec le contenu HTML fourni
    """
    if mail is None:
        print(f"⚠️ Flask-Mail non configuré. Email non envoyé à {to}")
        return False
    
    try:
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            html=html_content,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@theckmarket.com')
        )
        mail.send(msg)
        print(f"✅ Email envoyé à {to}: {subject}")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi email à {to}: {str(e)}")
        return False


# ============================================
# TEMPLATES D'EMAILS
# ============================================

def get_base_template(content, title=""):
    """Template de base pour tous les emails"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .header .logo {{
                font-size: 40px;
                margin-bottom: 10px;
            }}
            .content {{
                padding: 30px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 14px 28px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .button:hover {{
                opacity: 0.9;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .info-box {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            .success-box {{
                background: #d4edda;
                border-left: 4px solid #28a745;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
                color: #155724;
            }}
            .warning-box {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
                color: #856404;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}
            th {{
                background: #f8f9fa;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🛒</div>
                <h1>Theck Market</h1>
            </div>
            <div class="content">
                {content}
            </div>
            <div class="footer">
                <p>© {datetime.now().year} Theck Market - Tous droits réservés</p>
                <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
            </div>
        </div>
    </body>
    </html>
    """


# ============================================
# EMAILS UTILISATEURS
# ============================================

def send_welcome_email(user_email, user_name):
    """Email de bienvenue après inscription"""
    content = f"""
    <h2>🎉 Bienvenue {user_name} !</h2>
    <p>Merci de vous être inscrit sur <strong>Theck Market</strong>.</p>
    
    <div class="success-box">
        <strong>✅ Votre compte a été créé avec succès !</strong>
    </div>
    
    <p>Vous pouvez maintenant :</p>
    <ul>
        <li>🛍️ Parcourir notre catalogue de produits</li>
        <li>🛒 Ajouter des articles à votre panier</li>
        <li>💳 Effectuer des paiements sécurisés</li>
        <li>📦 Suivre vos commandes en temps réel</li>
    </ul>
    
    <p style="text-align: center;">
        <a href="https://staging-market.vercel.app/product" class="button">
            Découvrir nos produits →
        </a>
    </p>
    
    <div class="info-box">
        <strong>Besoin d'aide ?</strong><br>
        Notre équipe est disponible pour vous accompagner dans votre expérience d'achat.
    </div>
    """
    
    return send_email(
        to=user_email,
        subject="🎉 Bienvenue sur Theck Market !",
        html_content=get_base_template(content, "Bienvenue")
    )


def send_order_confirmation_email(user_email, user_name, order_details):
    """Email de confirmation de commande"""
    
    # Construire le tableau des produits
    products_rows = ""
    for item in order_details.get('items', []):
        products_rows += f"""
        <tr>
            <td>{item.get('name', 'Produit')}</td>
            <td style="text-align: center;">{item.get('quantity', 1)}</td>
            <td style="text-align: right;">{item.get('price', 0):,.0f} XAF</td>
        </tr>
        """
    
    content = f"""
    <h2>📦 Commande confirmée !</h2>
    <p>Bonjour <strong>{user_name}</strong>,</p>
    <p>Nous avons bien reçu votre commande et elle est en cours de préparation.</p>
    
    <div class="success-box">
        <strong>Référence :</strong> {order_details.get('reference', 'N/A')}<br>
        <strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    </div>
    
    <h3>📋 Détails de votre commande</h3>
    <table>
        <tr>
            <th>Produit</th>
            <th style="text-align: center;">Qté</th>
            <th style="text-align: right;">Prix</th>
        </tr>
        {products_rows}
        <tr style="font-weight: bold; background: #f8f9fa;">
            <td colspan="2">Total</td>
            <td style="text-align: right;">{order_details.get('total', 0):,.0f} XAF</td>
        </tr>
    </table>
    
    <div class="info-box">
        <strong>📍 Adresse de livraison :</strong><br>
        {order_details.get('address', 'Non spécifiée')}
    </div>
    
    <p style="text-align: center;">
        <a href="https://staging-market.vercel.app/order-tracking" class="button">
            Suivre ma commande →
        </a>
    </p>
    """
    
    return send_email(
        to=user_email,
        subject=f"📦 Commande confirmée - {order_details.get('reference', '')}",
        html_content=get_base_template(content, "Confirmation de commande")
    )


def send_delivery_confirmation_email(user_email, user_name, delivery_details):
    """Email de confirmation de livraison"""
    content = f"""
    <h2>✅ Livraison effectuée !</h2>
    <p>Bonjour <strong>{user_name}</strong>,</p>
    <p>Bonne nouvelle ! Votre commande a été livrée avec succès.</p>
    
    <div class="success-box">
        <strong>📦 Référence :</strong> {delivery_details.get('reference', 'N/A')}<br>
        <strong>📅 Date de livraison :</strong> {delivery_details.get('delivery_time', datetime.now().strftime('%d/%m/%Y à %H:%M'))}<br>
        <strong>💰 Montant :</strong> {delivery_details.get('amount', 0):,.0f} XAF
    </div>
    
    <p>Merci de votre confiance ! Nous espérons que vous êtes satisfait de votre achat.</p>
    
    <div class="info-box">
        <strong>💬 Donnez-nous votre avis !</strong><br>
        Votre retour nous aide à améliorer nos services.
    </div>
    
    <p style="text-align: center;">
        <a href="https://staging-market.vercel.app/product" class="button">
            Commander à nouveau →
        </a>
    </p>
    """
    
    return send_email(
        to=user_email,
        subject="✅ Votre commande a été livrée !",
        html_content=get_base_template(content, "Livraison confirmée")
    )


def send_password_reset_email(user_email, user_name, reset_token):
    """Email de réinitialisation de mot de passe"""
    reset_link = f"https://staging-market.vercel.app/reset-password?token={reset_token}"
    
    content = f"""
    <h2>🔐 Réinitialisation de mot de passe</h2>
    <p>Bonjour <strong>{user_name}</strong>,</p>
    <p>Vous avez demandé à réinitialiser votre mot de passe.</p>
    
    <p style="text-align: center;">
        <a href="{reset_link}" class="button">
            Créer un nouveau mot de passe →
        </a>
    </p>
    
    <div class="warning-box">
        <strong>⚠️ Attention :</strong><br>
        Ce lien expire dans <strong>1 heure</strong>.<br>
        Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
    </div>
    
    <p style="font-size: 12px; color: #666;">
        Si le bouton ne fonctionne pas, copiez ce lien dans votre navigateur :<br>
        <code style="background: #f5f5f5; padding: 5px;">{reset_link}</code>
    </p>
    """
    
    return send_email(
        to=user_email,
        subject="🔐 Réinitialisation de votre mot de passe",
        html_content=get_base_template(content, "Mot de passe")
    )


def send_payment_confirmation_email(user_email, user_name, payment_details):
    """Email de confirmation de paiement"""
    content = f"""
    <h2>💳 Paiement reçu !</h2>
    <p>Bonjour <strong>{user_name}</strong>,</p>
    <p>Nous avons bien reçu votre paiement.</p>
    
    <div class="success-box">
        <strong>Transaction :</strong> {payment_details.get('transaction_id', 'N/A')}<br>
        <strong>Montant :</strong> {payment_details.get('amount', 0):,.0f} {payment_details.get('currency', 'XAF')}<br>
        <strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    </div>
    
    <p>Votre commande sera préparée et expédiée dans les plus brefs délais.</p>
    
    <p style="text-align: center;">
        <a href="https://staging-market.vercel.app/order-tracking" class="button">
            Suivre ma commande →
        </a>
    </p>
    """
    
    return send_email(
        to=user_email,
        subject="💳 Paiement confirmé - Theck Market",
        html_content=get_base_template(content, "Paiement confirmé")
    )

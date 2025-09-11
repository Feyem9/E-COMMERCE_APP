import json
from flask import request, jsonify  #type:ignore Plus besoin de render_template ou redirect
from config import db , PAYUNIT_AUTHORIZATION , PAYUNIT_CONTENT_TYPE , PAYUNIT_BASE_URL , PAYUNIT_X_API_KEY , PAYUNIT_MODE , PAYUNIT_INITIATE_URL, SECRET_KEY, mail
from models.transaction_model import Transactions
import requests
import uuid
from datetime import datetime, timedelta
import qrcode # type: ignore
import io
import base64
from flask import send_file # type: ignore
import jwt
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore 
from flask_mail import Message # type: ignore

# Récupérer toutes les transactions


def generate_transaction_id():
    return f"4478-{uuid.uuid4().hex[:6]}"  # par exemple : "4478-a1b2c3"
def index():
    transactions = Transactions.query.all()
    return jsonify([transaction.serialize() for transaction in transactions]), 200

# Récupérer une transaction par ID
def view_transaction(transaction_id):
    transaction = Transactions.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction non trouvée'}), 404
    return jsonify(transaction.serialize()), 200

# Mettre à jour une transaction
def update_transaction(transaction_id):
    transaction = Transactions.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction non trouvée'}), 404

    data = request.get_json()
    status = data.get('status')
    if status:
        transaction.status = status
        db.session.commit()
        return jsonify({'message': 'Transaction mise à jour avec succès', 'transaction': transaction.serialize()}), 200
    return jsonify({'error': 'Champ "status" manquant'}), 400

# Supprimer une transaction
def delete_transaction(transaction_id):
    transaction = Transactions.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction non trouvée'}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction supprimée avec succès'}), 200


# def initiate_payment():
#     data = request.get_json()

#     required_fields = ['total_amount', 'currency', 'transaction_id', 'return_url']
#     for field in required_fields:
#         if field not in data:
#             return jsonify({'error': f'Missing field: {field}'}), 400
        
#         # Génère un identifiant unique pour cette transaction
#         transaction_id = generate_transaction_id()
        
#     payload = json.dumps({
#         "total_amount" : data['total_amount'],
#         "currency" : data['currency'],
#         "transaction_id" : transaction_id,
#         "return_url" : data['return_url'],
#         "notify_url":data['notify_url'],
#         "payment_country":data['payment_country']
#     }) 
 
#     headers = {
#         "x-api-key": PAYUNIT_X_API_KEY,
#         "mode": PAYUNIT_MODE,
#         "Content-Type": PAUNIT_CONTENT_TYPE,
#         "Authorization": PAYUNIT_AUTHORIZATION
#     }
#     print("🔁 Lien de redirection vers PayUnit:", PAYUNIT_INITIATE_URL)
#     print("🔁 L authorization key vers PayUnit:", PAYUNIT_X_API_KEY)
#     print("content type:", PAUNIT_CONTENT_TYPE)
#     print("mode:", PAYUNIT_MODE)
#     print("payload:", payload)
#     print("headers:", headers)
#     print("data:", data)

#     try:
#         response = requests.request(
#             "POST",
#             PAYUNIT_INITIATE_URL,  # ne pas ajouter /initiate à la fin
#             data=payload,
#             headers=headers
#         )
        
        
#         print("response:", response)
#         print("Réponse brute PayUnit ➜", response.text)
#         print("Status:", response.status_code)

#         if response.status_code == 200:
#             result = response.json()

#             # Enregistrement
#             new_transaction = Transactions(transaction_id=data['transaction_id']
#                                           , total_amount=data['total_amount'],
#                                           currency=data['currency'],
#                                           status="pending",
#                                           redirect_url=result.get("redirect_url"))
            
#             db.session.add(new_transaction)
#             db.session.commit()
#             print("Réponse PayUnit:", result)   

#             return jsonify({
#                 "message": "Paiement initié avec succès.",
#                 "payment_url": result["data"].get("transaction_url"),
#                 "transaction_id": new_transaction.transaction_id,
#                 "return_url": result["data"].get("t_url"),
#                 "data": {
#                     "t_id": result["data"].get("t_id"),
#                     "t_sum": result["data"].get("t_sum"),
#                     "t_url": result["data"].get("t_url"),
#                     "transaction_id": result["data"].get("transaction_id"),
#                     "transaction_url": result["data"].get("transaction_url")
#                 }
#             }), 200


#         else:
#             return jsonify({
#                 "error": "Échec de l'initialisation du paiement",
#                 "details": response.text
#             }), 500

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

def initiate_payment():
    data = request.get_json()

    # ✅ Étape 1 : Vérifier les champs nécessaires (sans 'transaction_id')
    required_fields = ['total_amount', 'currency', 'return_url', 'notify_url', 'payment_country']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # ✅ Étape 2 : Générer un ID de transaction unique
    transaction_id = generate_transaction_id()

    # ✅ Étape 3 : Construire le payload pour PayUnit
    payload = json.dumps({
        "total_amount": data['total_amount'],
        "currency": data['currency'],
        "transaction_id": transaction_id,
        "return_url": data['return_url'],
        "notify_url": data['notify_url'],
        "payment_country": data['payment_country']
    })

    headers = {
        "x-api-key": PAYUNIT_X_API_KEY,
        "mode": PAYUNIT_MODE,
        "Content-Type": PAYUNIT_CONTENT_TYPE,
        "Authorization": PAYUNIT_AUTHORIZATION
    }

    print("🔁 Payload envoyé à PayUnit:", payload)

    try:
        response = requests.post(PAYUNIT_INITIATE_URL, data=payload, headers=headers)

        print("Réponse PayUnit brut ➜", response.text)
        print("Status HTTP:", response.status_code)

        if response.status_code == 200:
            result = response.json()

            # ✅ Étape 4 : Enregistrer la transaction dans la base
            new_transaction = Transactions(
                transaction_id=transaction_id,
                total_amount=data['total_amount'],
                currency=data['currency'],
                status="pending",
                redirect_url=result["data"].get("transaction_url")
            )
            db.session.add(new_transaction)
            db.session.commit()

            # ✅ Étape 5 : Retourner la réponse au frontend
            return jsonify({
                "message": "Paiement initié avec succès.",
                "payment_url": result["data"].get("transaction_url"),
                "transaction_id": transaction_id,
                "return_url": result["data"].get("t_url"),
                "data": {
                    "t_id": result["data"].get("t_id"),
                    "t_sum": result["data"].get("t_sum"),
                    "t_url": result["data"].get("t_url"),
                    "transaction_id": result["data"].get("transaction_id"),
                    "transaction_url": result["data"].get("transaction_url")
                }
            }), 200

        else:
            return jsonify({
                "error": "Échec de l'initialisation du paiement",
                "details": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Génération d’un token sécurisé
def generate_qr_token(transaction_id):
    payload = {
        "transaction_id": transaction_id,
        "exp": datetime.utcnow() + timedelta(minutes=10)  # QR valide 10 min
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Nouvelle route backend : Génération du QR Code
def generate_qrcode(transaction_id):
    transaction = Transactions.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({"error": "Transaction non trouvée"}), 404

    token = generate_qr_token(transaction_id)

    qr_data = {
        "transaction_id": transaction_id,
        "token": token
    }

    # Générer le QR code en mémoire
    qr_img = qrcode.make(json.dumps(qr_data))
    img_io = io.BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

def confirm_transaction():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token manquant"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        transaction_id = decoded["transaction_id"]

        transaction = Transactions.query.filter_by(transaction_id=transaction_id).first()
        if not transaction:
            return jsonify({"error": "Transaction non trouvée"}), 404

        transaction.status = "paid"
        db.session.commit()

        return jsonify({"message": "Transaction validée avec succès", "transaction": transaction.serialize()}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "QR Code expiré"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide"}), 400



def generate_invoice_pdf(transaction):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Facture N° {transaction.transaction_id}")
    c.drawString(100, 720, f"Montant : {transaction.total_amount} {transaction.currency}")
    c.drawString(100, 700, f"Statut : {transaction.status}")
    c.drawString(100, 680, f"Date : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def send_invoice(transaction, client_email, admin_email="admin@museschool.com"):
    pdf_buffer = generate_invoice_pdf(transaction)

    msg = Message("Votre facture", recipients=[client_email, admin_email])
    msg.body = f"Merci pour votre paiement. Facture N° {transaction.transaction_id}"
    msg.attach(f"facture_{transaction.transaction_id}.pdf", "application/pdf", pdf_buffer.read())

    mail.send(msg)
    return jsonify({"message": "Facture envoyée par email"}), 200


def user_transactions(user_id):
    transactions = Transactions.query.filter_by(user_id=user_id).all()
    return jsonify([t.serialize() for t in transactions]), 200


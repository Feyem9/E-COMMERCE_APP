import json
from flask import request, jsonify  #type:ignore Plus besoin de render_template ou redirect
from config import db , PAYUNIT_AUTHORIZATION , PAUNIT_CONTENT_TYPE , PAYUNIT_BASE_URL , PAYUNIT_X_API_KEY , PAYUNIT_MODE , PAYUNIT_INITIATE_URL
from models.transaction_model import Transactions
import requests
import uuid
from datetime import datetime

# Récupérer toutes les transactions


def generate_transaction_id():
    return f"4478-{uuid.uuid4().hex[:6]}"  # Revenir à 6 caractères qui fonctionnait
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
    # Convertir le montant en float et formater à 2 décimales pour éviter les problèmes de précision
    amount = float(data['total_amount'])
    formatted_amount = "{:.2f}".format(amount)

    payload = json.dumps({
        "total_amount": formatted_amount,
        "currency": data['currency'],
        "transaction_id": transaction_id,
        "return_url": data['return_url'],
        "notify_url": data['notify_url'],
        "payment_country": data['payment_country']
    })

    headers = {
        "x-api-key": PAYUNIT_X_API_KEY,
        "mode": PAYUNIT_MODE,
        "Content-Type": PAUNIT_CONTENT_TYPE,
        "Authorization": PAYUNIT_AUTHORIZATION
    }

    print("🔁 Payload envoyé à PayUnit:", payload)

    try:
        # Créer la table si elle n'existe pas (pour SQLite)
        try:
            db.create_all()
        except Exception as e:
            print(f"⚠️  Erreur lors de la création des tables: {e}")

        response = requests.post(PAYUNIT_INITIATE_URL, data=payload, headers=headers)

        print("Réponse PayUnit brut ➜", response.text)
        print("Status HTTP:", response.status_code)

        if response.status_code == 200:
            result = response.json()

            # ✅ Étape 4 : Enregistrer la transaction dans la base
            try:
                new_transaction = Transactions(
                    transaction_id=transaction_id,
                    total_amount=data['total_amount'],
                    currency=data['currency'],
                    status="pending",
                    redirect_url=result["data"].get("transaction_url")
                )
                db.session.add(new_transaction)
                db.session.commit()
                print("✅ Transaction enregistrée avec succès")
            except Exception as e:
                print(f"❌ Erreur lors de l'enregistrement de la transaction: {e}")
                return jsonify({"error": f"Erreur de base de données: {str(e)}"}), 500

            # ✅ Étape 5 : Retourner la réponse au frontend
            try:
                response_data = {
                    "message": "Paiement initié avec succès.",
                    "payment_url": result["data"].get("transaction_url"),
                    "transaction_id": transaction_id,
                    "return_url": result["data"].get("t_url"),
                    "data": {
                        "t_id": result["data"].get("t_id"),
                        "t_sum": result["data"].get("t_sum"),
                        "t_url": result["data"].get("t_url"),
                        "transaction_id": transaction_id,  # Utiliser notre transaction_id généré
                        "transaction_url": result["data"].get("transaction_url")
                    }
                }
                print("✅ Réponse finale préparée:", response_data)
                return jsonify(response_data), 200
            except Exception as e:
                print(f"❌ Erreur lors de la préparation de la réponse: {e}")
                return jsonify({"error": f"Erreur de réponse: {str(e)}"}), 500

        else:
            return jsonify({
                "error": "Échec de l'initialisation du paiement",
                "details": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour valider une transaction via QR code
def validate_transaction():
    data = request.get_json()
    qr_code = data.get('qr_code')

    if not qr_code:
        return jsonify({'error': 'QR code manquant'}), 400

    # Rechercher la transaction par son ID (le QR code contient l'ID de transaction)
    transaction = Transactions.query.filter_by(transaction_id=qr_code).first()

    if not transaction:
        return jsonify({'error': 'Transaction non trouvée'}), 404

    # Vérifier que la transaction est en attente de validation
    if transaction.status != 'pending':
        return jsonify({'error': f'Transaction déjà {transaction.status}'}), 400

    # Mettre à jour le statut de la transaction
    transaction.status = 'completed'
    db.session.commit()

    return jsonify({
        'message': 'Transaction validée avec succès',
        'transaction_id': transaction.transaction_id,
        'status': transaction.status,
        'amount': transaction.total_amount,
        'currency': transaction.currency
    }), 200

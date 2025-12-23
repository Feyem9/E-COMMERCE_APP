import json
from flask import request, jsonify  #type:ignore Plus besoin de render_template ou redirect
from config import db , PAYUNIT_AUTHORIZATION , PAUNIT_CONTENT_TYPE , PAYUNIT_BASE_URL , PAYUNIT_X_API_KEY , PAYUNIT_MODE , PAYUNIT_INITIATE_URL
from models.transaction_model import Transactions
import requests
import uuid
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from utils.qr_security import generate_qr_data  # 🔐 QR Code sécurisé

# Récupérer toutes les transactions
from math import radians, cos, sin, asin, sqrt

# ✅ Calcul de distance GPS (formule Haversine)
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en km entre deux points GPS
    lat1, lon1: Position client
    lat2, lon2: Position entrepôt/point de livraison
    """
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    try:
        # Convertir en radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # Formule Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Rayon de la Terre en km
        km = 6371 * c
        return round(km, 2)
    except Exception as e:
        print(f"⚠️ Erreur calcul distance: {e}")
        return None



def generate_transaction_id():
    return f"4478-{uuid.uuid4().hex[:6]}"

# 🗺️ Génération lien Google Maps pour itinéraire
def generate_delivery_map_url(origin_lat, origin_lng, dest_lat, dest_lng):
    """
    Génère un lien Google Maps avec directions pour le livreur
    origin: Position entrepôt/départ
    dest: Position client/arrivée
    """
    if not all([origin_lat, origin_lng, dest_lat, dest_lng]):
        return None
    
    try:
        # Format: https://www.google.com/maps/dir/ORIGIN/DESTINATION
        base_url = "https://www.google.com/maps/dir/"
        origin = f"{origin_lat},{origin_lng}"
        destination = f"{dest_lat},{dest_lng}"
        
        map_url = f"{base_url}{origin}/{destination}"
        return map_url
    except Exception as e:
        print(f"⚠️ Erreur génération lien maps: {e}")
        return None

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
                # Coordonnées de l'entrepôt/point de livraison (Yaoundé, Cameroun)
                WAREHOUSE_LAT = 3.8689
                WAREHOUSE_LNG = 11.5213
                
                # Récupérer coordonnées client
                customer_lat = data.get('customer_latitude')
                customer_lng = data.get('customer_longitude')
                
                # Calculer distance et générer itinéraire si coordonnées disponibles
                distance_km = None
                delivery_map = None
                
                if customer_lat and customer_lng:
                    # Calcul distance
                    distance_km = calculate_distance(
                        customer_lat, customer_lng,
                        WAREHOUSE_LAT, WAREHOUSE_LNG
                    )
                    
                    # Génération lien Google Maps pour itinéraire
                    delivery_map = generate_delivery_map_url(
                        WAREHOUSE_LAT, WAREHOUSE_LNG,  # Départ: Entrepôt
                        customer_lat, customer_lng      # Arrivée: Client
                    )
                    
                    print(f"📍 Position client: ({customer_lat}, {customer_lng})")
                    print(f"📍 Distance de livraison: {distance_km} km")
                    print(f"🗺️ Itinéraire Maps: {delivery_map}")
                
                # 🔐 Générer QR code sécurisé
                temp_transaction = Transactions(
                    transaction_id=transaction_id,
                    total_amount=data['total_amount'],
                    currency=data['currency'],
                    status="pending",
                    redirect_url=result["data"].get("transaction_url")
                )
                
                qr_data, signature, reference = generate_qr_data(temp_transaction)
                print(f"🔐 Signature: {signature[:20]}... Réf: {reference}")
                
                new_transaction = Transactions(
                    transaction_id=transaction_id,
                    total_amount=data['total_amount'],
                    currency=data['currency'],
                    status="pending",
                    redirect_url=result["data"].get("transaction_url"),
                    customer_latitude=customer_lat,
                    customer_longitude=customer_lng,
                    delivery_distance_km=distance_km,
                    delivery_map_url=delivery_map,
                    qr_signature=signature,
                    reference=reference
                )
                db.session.add(new_transaction)
                db.session.commit()
                print(f"✅ Transaction {reference} enregistrée")
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

def validate_transaction():
    """Valide une livraison via scan QR code sécurisé"""
    from utils.qr_security import validate_qr_data
    from datetime import datetime
    
    data = request.get_json()
    qr_string = data.get('qr_code')
    
    if not qr_string:
        return jsonify({"error": "QR code manquant"}), 400
    
    # Valider QR code (signature HMAC)
    is_valid, qr_data, error = validate_qr_data(qr_string)
    
    if not is_valid:
        return jsonify({"error": f"QR invalide: {error}"}), 400
    
    # Chercher transaction
    transaction = Transactions.query.filter_by(
        transaction_id=qr_data['transaction_id']
    ).first()
    
    if not transaction:
        return jsonify({"error": "Transaction introuvable"}), 404
    
    # Vérifier signature en BDD
    if transaction.qr_signature != qr_data['signature']:
        return jsonify({"error": "Signature ne correspond pas"}), 400
    
    # Vérifier si déjà livrée
    if transaction.status == "success":
        return jsonify({
            "error": "Livraison déjà validée",
            "delivery_time": transaction.delivery_time.isoformat() if transaction.delivery_time else None
        }), 400
    
    # Vérifier status valide
    if transaction.status not in ["pending", "confirmed"]:
        return jsonify({"error": f"Status invalide: {transaction.status}"}), 400
    
    # VALIDER LA LIVRAISON
    transaction.status = "success"
    transaction.delivery_time = datetime.now()
    
    try:
        db.session.commit()
        
        print(f"✅ Livraison validée: {transaction.reference}")
        
        return jsonify({
            "message": "✅ Livraison confirmée avec succès !",
            "transaction_id": transaction.transaction_id,
            "reference": transaction.reference,
            "amount": transaction.total_amount,
            "currency": transaction.currency,
            "delivery_time": transaction.delivery_time.isoformat(),
            "distance": transaction.delivery_distance_km
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur: {str(e)}"}), 500


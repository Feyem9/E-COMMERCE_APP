"""
🔐 Utilitaires QR Code Sécurisé
Génération et validation de QR codes avec signature HMAC
"""

import hmac
import hashlib
import json
import base64
from datetime import datetime

# Clé secrète pour HMAC (⚠️ À mettre dans .env en production !)
QR_SECRET_KEY = "your-super-secret-key-change-in-production-2025"

def generate_qr_signature(transaction_id, amount, currency, timestamp):
    """
    Génère une signature HMAC-SHA256 pour sécuriser le QR code
    
    Args:
        transaction_id: ID unique de la transaction
        amount: Montant de la transaction
        currency: Devise
        timestamp: Horodatage ISO format
    
    Returns:
        str: Signature hexadécimale
    """
    # Créer le message à signer
    message = f"{transaction_id}|{amount}|{currency}|{timestamp}"
    
    # Générer HMAC-SHA256
    signature = hmac.new(
        QR_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature


def verify_qr_signature(transaction_id, amount, currency, timestamp, signature):
    """
    Vérifie la validité d'une signature QR code
    
    Args:
        transaction_id: ID de la transaction
        amount: Montant
        currency: Devise
        timestamp: Horodatage
        signature: Signature à vérifier
    
    Returns:
        bool: True si signature valide
    """
    # Régénérer la signature
    expected_signature = generate_qr_signature(transaction_id, amount, currency, timestamp)
    
    # Comparaison sécurisée (évite timing attacks)
    return hmac.compare_digest(signature, expected_signature)


def generate_qr_data(transaction):
    """
    Génère les données complètes du QR code
    
    Args:
        transaction: Objet Transaction
    
    Returns:
        dict: Données pour le QR code
    """
    timestamp = datetime.now().isoformat()
    
    # Générer signature
    signature = generate_qr_signature(
        transaction.transaction_id,
        transaction.total_amount,
        transaction.currency,
        timestamp
    )
    
    # Créer référence commande
    reference = f"CMD-{datetime.now().strftime('%Y%m%d')}-{transaction.transaction_id[-6:]}"
    
    qr_data = {
        "transaction_id": transaction.transaction_id,
        "reference": reference,
        "amount": transaction.total_amount,
        "currency": transaction.currency,
        "status": transaction.status,
        "timestamp": timestamp,
        "signature": signature
    }
    
    return qr_data, signature, reference


def qr_data_to_string(qr_data):
    """
    Convertit les données QR en string JSON
    
    Args:
        qr_data: Dictionnaire des données
    
    Returns:
        str: JSON string pour QR code
    """
    return json.dumps(qr_data, ensure_ascii=False)


def validate_qr_data(qr_string):
    """
    Valide et décode un QR code scanné
    
    Args:
        qr_string: String JSON du QR code
    
    Returns:
        tuple: (is_valid, qr_data_dict, error_message)
    """
    try:
        # Décoder JSON
        qr_data = json.loads(qr_string)
        
        # Vérifier champs obligatoires
        required_fields = ['transaction_id', 'amount', 'currency', 'timestamp', 'signature']
        for field in required_fields:
            if field not in qr_data:
                return False, None, f"Champ manquant: {field}"
        
        # Vérifier signature
        is_valid = verify_qr_signature(
            qr_data['transaction_id'],
            qr_data['amount'],
            qr_data['currency'],
            qr_data['timestamp'],
            qr_data['signature']
        )
        
        if not is_valid:
            return False, None, "Signature invalide - QR code non authentique"
        
        return True, qr_data, None
        
    except json.JSONDecodeError as e:
        return False, None, f"Format JSON invalide: {str(e)}"
    except Exception as e:
        return False, None, f"Erreur validation: {str(e)}"

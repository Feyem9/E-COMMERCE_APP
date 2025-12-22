#!/usr/bin/env python3
"""
Script de modification rapide pour ajouter QR code sécurisé
"""

import re

# Lire le fichier
with open('controllers/transaction_controller.py', 'r') as f:
    content = f.read()

# 1. Ajouter import en haut (après les autres imports)
if 'from utils.qr_security import generate_qr_data' not in content:
    # Trouver la ligne après les imports
    content = content.replace(
        'from sqlalchemy import text',
        'from sqlalchemy import text\nfrom utils.qr_security import generate_qr_data'
    )

# 2. Modifier la création de transaction
old_code = '''                new_transaction = Transactions(
                    transaction_id=transaction_id,
                    total_amount=data['total_amount'],
                    currency=data['currency'],
                    status="pending",
                    redirect_url=result["data"].get("transaction_url"),
                    customer_latitude=customer_lat,
                    customer_longitude=customer_lng,
                    delivery_distance_km=distance_km,
                    delivery_map_url=delivery_map
                )
                db.session.add(new_transaction)
                db.session.commit()
                print("✅ Transaction enregistrée avec succès")'''

new_code = '''                # 🔐 Générer QR code sécurisé
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
                print(f"✅ Transaction {reference} enregistrée")'''

content = content.replace(old_code, new_code)

# 3. Ajouter qr_data dans response
old_response = '''                response_data = {
                    "message": "Paiement initié avec succès.",
                    "payment_url": result["data"].get("transaction_url"),
                    "transaction_id": transaction_id,
                    "return_url": result["data"].get("t_url"),
                    "t_id": result["data"].get("t_id")
                }'''

new_response = '''                response_data = {
                    "message": "Paiement initié avec succès.",
                    "payment_url": result["data"].get("transaction_url"),
                    "transaction_id": transaction_id,
                    "return_url": result["data"].get("t_url"),
                    "t_id": result["data"].get("t_id"),
                    "qr_data": qr_data  # 🔐 QR sécurisé
                }'''

content = content.replace(old_response, new_response)

# Écrire le résultat
with open('controllers/transaction_controller.py', 'w') as f:
    f.write(content)

print("✅ Modifications appliquées!")
print("   - Import qr_security ajouté")
print("   - Génération QR dans initiate_payment")
print("   - qr_data ajouté à la response")

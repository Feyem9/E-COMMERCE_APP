#!/usr/bin/env python3
"""
Script pour remplacer validate_transaction() avec version sécurisée
"""

# Lire le fichier
with open('controllers/transaction_controller.py', 'r') as f:
    lines = f.readlines()

# Trouver la fonction validate_transaction
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if 'def validate_transaction' in line:
        start_idx = i - 1  # Capture @app.route aussi
    elif start_idx and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
        end_idx = i
        break

if not start_idx:
    print("❌ validate_transaction non trouvée")
    exit(1)

# Nouvelle fonction
new_function = '''@app.route('/transactions/validate', methods=['POST'])
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

'''

# Remplacer
if end_idx:
    new_lines = lines[:start_idx] + [new_function] + lines[end_idx:]
else:
    new_lines = lines[:start_idx] + [new_function]

# Écrire
with open('controllers/transaction_controller.py', 'w') as f:
    f.writelines(new_lines)

print("✅ validate_transaction() remplacée!")
print("   - Validation signature HMAC")
print("   - Vérification double (signature + BDD)")
print("   - Status → success")
print("   - delivery_time enregistré")

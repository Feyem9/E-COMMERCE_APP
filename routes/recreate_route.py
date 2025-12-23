"""
🔧 ENDPOINT TEMPORAIRE - Force Recreation Table Transactions
⚠️ SUPPRIME TOUTES LES DONNÉES TRANSACTIONS !
"""

from flask import Blueprint, jsonify
from config import db
from sqlalchemy import text

recreate_bp = Blueprint('recreate', __name__)

@recreate_bp.route('/admin/recreate-transactions', methods=['GET'])
def recreate_transactions():
    """
    ⚠️ DESTRUCTIF : Supprime et recrée la table transactions
    Utiliser UNIQUEMENT si table corrompue ou colonnes manquantes
    """
    try:
        # 1. Supprimer la table
        db.session.execute(text('DROP TABLE IF EXISTS transactions'))
        db.session.commit()
        print("✅ Table transactions supprimée")
        
        # 2. Recréer avec db.create_all()
        from models.transaction_model import Transactions
        db.create_all()
        print("✅ Table transactions recréée avec toutes les colonnes")
        
        # 3. Vérifier les colonnes
        result = db.session.execute(text("PRAGMA table_info(transactions)"))
        columns = [row[1] for row in result]
        
        return jsonify({
            "status": "success",
            "message": "✅ Table transactions recréée avec succès !",
            "columns": columns,
            "warning": "⚠️ Toutes les anciennes données ont été supprimées"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"❌ Erreur: {str(e)}"
        }), 500

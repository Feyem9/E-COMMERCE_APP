"""
🔧 ENDPOINT TEMPORAIRE - Migration BDD Géolocalisation
⚠️ À SUPPRIMER après utilisation !
"""

from flask import Blueprint, jsonify
from config import db
from sqlalchemy import text

migrate_bp = Blueprint('migrate', __name__)

@migrate_bp.route('/admin/migrate-geoloc', methods=['GET'])
def migrate_geoloc():
    """Ajoute les colonnes de géolocalisation à la table transactions"""
    try:
        # ALTER TABLE pour ajouter les colonnes manquantes
        db.session.execute(text('''
            ALTER TABLE transactions 
            ADD COLUMN IF NOT EXISTS customer_latitude FLOAT,
            ADD COLUMN IF NOT EXISTS customer_longitude FLOAT,
            ADD COLUMN IF NOT EXISTS delivery_distance_km FLOAT,
            ADD COLUMN IF NOT EXISTS delivery_map_url VARCHAR(500)
        '''))
        db.session.commit()
        
        return jsonify({
            "status": "success", 
            "message": "✅ Colonnes de géolocalisation ajoutées avec succès!",
            "columns_added": [
                "customer_latitude",
                "customer_longitude", 
                "delivery_distance_km",
                "delivery_map_url"
            ]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        
        # Si les colonnes existent déjà, c'est OK
        if "already exists" in error_msg or "duplicate column" in error_msg.lower():
            return jsonify({
                "status": "success",
                "message": "✅ Colonnes déjà existantes - Migration OK!",
                "note": "Les colonnes étaient déjà présentes dans la base."
            }), 200
        
        return jsonify({
            "status": "error",
            "message": f"❌ Erreur lors de la migration: {error_msg}"
        }), 500

"""
🔧 ENDPOINT TEMPORAIRE - Migration BDD Géolocalisation (SQLite Compatible)
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
        columns_to_add = [
            ('customer_latitude', 'FLOAT'),
            ('customer_longitude', 'FLOAT'),
            ('delivery_distance_km', 'FLOAT'),
            ('delivery_map_url', 'VARCHAR(500)')
        ]
        
        added_columns = []
        skipped_columns = []
        
        # Pour SQLite, on doit ajouter les colonnes une par une (pas de IF NOT EXISTS)
        for column_name, column_type in columns_to_add:
            try:
                # SQLite: ALTER TABLE ... ADD COLUMN (sans IF NOT EXISTS)
                sql = f'ALTER TABLE transactions ADD COLUMN {column_name} {column_type}'
                db.session.execute(text(sql))
                db.session.commit()
                added_columns.append(column_name)
            except Exception as e:
                error_msg = str(e).lower()
                # Si la colonne existe déjà, c'est OK
                if 'duplicate' in error_msg or 'already exists' in error_msg or 'duplicate column' in error_msg:
                    skipped_columns.append(column_name)
                    db.session.rollback()
                else:
                    # Autre erreur, on re-raise
                    raise
        
        if added_columns:
            return jsonify({
                "status": "success", 
                "message": f"✅ {len(added_columns)} colonnes ajoutées avec succès!",
                "columns_added": added_columns,
                "columns_skipped": skipped_columns
            }), 200
        else:
            return jsonify({
                "status": "success",
                "message": "✅ Toutes les colonnes existaient déjà - Migration OK!",
                "columns_skipped": skipped_columns
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": f"❌ Erreur lors de la migration: {str(e)}"
        }), 500

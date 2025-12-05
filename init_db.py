"""
Script pour initialiser la base de données avec les produits
Exécuté automatiquement lors du premier démarrage
"""
import os
import sys

def init_db():
    """Initialiser la base de données avec les données de produits"""
    try:
        from app import app, db
        from models.product_model import Products
        
        with app.app_context():
            # Vérifier si la table products existe et contient des données
            existing_count = Products.query.count()
            
            if existing_count == 0:
                print("🌱 Peuplement de la base de données...")
                from populate_db import populate_products
                populate_products()
            else:
                print(f"✅ Base de données déjà peuplée ({existing_count} produits)")
                
    except Exception as e:
        print(f"⚠️  Erreur lors de l'initialisation: {e}")
        # Ne pas arrêter l'app si l'initialisation échoue
        pass

if __name__ == '__main__':
    init_db()

#!/usr/bin/env python3
"""
Script pour créer toutes les tables PostgreSQL
"""
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def create_all_tables():
    """Créer toutes les tables dans la base de données"""
    with app.app_context():
        # Importer tous les modèles pour s'assurer qu'ils sont enregistrés
        from models.customer_model import Customers
        from models.product_model import Products
        from models.cart_model import Carts
        from models.category_model import Categories
        from models.favorite_model import Favorites
        from models.order_model import Orders
        from models.transaction_model import Transactions
        
        try:
            # Créer toutes les tables
            db.create_all()
            print("✅ Toutes les tables ont été créées avec succès!")
            print("Tables créées:")
            
            # Lister les tables créées
            tables = db.metadata.tables.keys()
            for table in tables:
                print(f"  - {table}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la création des tables: {e}")

if __name__ == "__main__":
    create_all_tables()
#!/usr/bin/env python3
"""
Script d'initialisation propre pour PostgreSQL sur Render
Crée toutes les tables directement sans migrations conflictuelles
"""
import os
from flask import Flask
from flask_migrate import stamp

def deploy():
    """Déploiement propre pour PostgreSQL."""
    
    # Importer l'app et la DB
    from app import app, db
    
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
            print("🚀 Initialisation PostgreSQL...")
            
            # Créer toutes les tables directement
            db.create_all()
            
            print("✅ Tables créées avec succès!")
            
            # Marquer comme étant à la dernière migration
            stamp()
            
            print("✅ Migrations marquées comme appliquées!")
            print("🎉 Déploiement PostgreSQL terminé!")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            raise e

if __name__ == '__main__':
    deploy()
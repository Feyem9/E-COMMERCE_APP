#!/usr/bin/env python3
"""
Script d'initialisation pour Render - PostgreSQL
Ce script sera exécuté lors du déploiement sur Render
"""
import os
from flask import Flask

def deploy():
    """Exécuter les déploiements."""
    
    # Importer l'app
    from app import app, db
    
    with app.app_context():
        # Importer tous les modèles
        from models.customer_model import Customers
        from models.product_model import Products
        from models.cart_model import Carts
        from models.category_model import Categories
        from models.favorite_model import Favorites
        from models.order_model import Orders
        from models.transaction_model import Transactions
        
        print("🚀 Initialisation de la base de données PostgreSQL...")
        
        # Créer toutes les tables
        db.create_all()
        
        print("✅ Déploiement terminé! Tables créées:")
        print("  - customers")
        print("  - products") 
        print("  - carts")
        print("  - categories")
        print("  - favorites")
        print("  - orders")
        print("  - transactions")

if __name__ == '__main__':
    deploy()
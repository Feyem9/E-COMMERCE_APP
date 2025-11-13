#!/usr/bin/env python3
"""
Script de déploiement avec population de données
À exécuter sur Render pour peupler la base de données PostgreSQL
"""
import os
from flask import Flask

def deploy_with_data():
    """Déploiement avec population de données"""
    
    # Importer l'app et les modèles
    from app import app, db
    from models.customer_model import Customers
    from models.product_model import Products
    from models.cart_model import Carts
    from models.category_model import Categories
    from models.favorite_model import Favorites
    from models.order_model import Orders
    from models.transaction_model import Transactions
    
    with app.app_context():
        print("🚀 Initialisation PostgreSQL avec données...")
        
        # Créer toutes les tables
        db.create_all()
        print("✅ Tables créées!")
        
        # Vérifier si la base est vide
        product_count = Products.query.count()
        print(f"📊 Produits existants: {product_count}")
        
        if product_count == 0:
            print("📱 Ajout des produits smartphones...")
            phone_products = [
                {'name': 'iPhone 15 Pro', 'description': 'Latest iPhone with titanium design and A17 Pro chip', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000000/ecommerce/iphone15pro.jpg'},
                {'name': 'iPhone 15', 'description': 'Powerful iPhone with Dynamic Island and USB-C', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000001/ecommerce/iphone15.jpg'},
                {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Ultimate Android flagship with S Pen', 'current_price': 1299.99, 'discount_price': 1199.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000003/ecommerce/galaxys24ultra.jpg'},
                {'name': 'Google Pixel 8 Pro', 'description': 'AI-powered camera with 7 years of updates', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000006/ecommerce/pixel8pro.jpg'},
                {'name': 'OnePlus 12', 'description': 'Fast charging flagship with Hasselblad camera', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000008/ecommerce/oneplus12.jpg'},
                {'name': 'Xiaomi 14', 'description': 'Leica camera partnership with Snapdragon 8 Gen 3', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000009/ecommerce/xiaomi14.jpg'},
                {'name': 'iPhone SE (3rd gen)', 'description': 'Affordable iPhone with A15 Bionic', 'current_price': 429.99, 'discount_price': 379.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000020/ecommerce/iphonese.jpg'},
                {'name': 'Samsung Galaxy A54', 'description': 'Mid-range Android with IP67 rating', 'current_price': 349.99, 'discount_price': 299.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000021/ecommerce/galaxya54.jpg'},
                {'name': 'Google Pixel 7a', 'description': 'Budget Pixel with Tensor G2', 'current_price': 499.99, 'discount_price': 449.99, 'quantity': 28, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000022/ecommerce/pixel7a.jpg'},
                {'name': 'Nokia G42', 'description': 'Budget phone with 3 years of updates', 'current_price': 199.99, 'discount_price': 149.99, 'quantity': 45, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000033/ecommerce/nokiag42.jpg'},
            ]
            
            success_count = 0
            for product_data in phone_products:
                try:
                    product = Products(**product_data)
                    db.session.add(product)
                    success_count += 1
                except Exception as e:
                    print(f"❌ Erreur: {product_data['name']} - {e}")
            
            try:
                db.session.commit()
                print(f"✅ {success_count} produits ajoutés!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erreur commit: {e}")
        else:
            print("⏭️  Base déjà peuplée, passage...")
        
        print("🎉 Déploiement avec données terminé!")

if __name__ == '__main__':
    deploy_with_data()
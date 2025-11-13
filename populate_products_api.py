#!/usr/bin/env python3
"""
Script pour peupler la base de données PostgreSQL avec les produits
Utilise la même liste de produits que populate_db.py mais adapté pour PostgreSQL
"""
import os
import requests
import json

# Configuration pour utiliser l'API distante
API_BASE_URL = "https://e-commerce-app-1-islr.onrender.com"

def populate_products_via_api():
    """Ajouter des produits via l'API REST"""
    
    phone_products = [
        {'name': 'iPhone 15 Pro', 'description': 'Latest iPhone with titanium design and A17 Pro chip', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000000/ecommerce/iphone15pro.jpg'},
        {'name': 'iPhone 15', 'description': 'Powerful iPhone with Dynamic Island and USB-C', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000001/ecommerce/iphone15.jpg'},
        {'name': 'iPhone 14 Pro', 'description': 'Pro camera system with 48MP sensor', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000002/ecommerce/iphone14pro.jpg'},
        {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Ultimate Android flagship with S Pen', 'current_price': 1299.99, 'discount_price': 1199.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000003/ecommerce/galaxys24ultra.jpg'},
        {'name': 'Samsung Galaxy S24+', 'description': 'Large screen Android phone with AI features', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000004/ecommerce/galaxys24plus.jpg'},
        {'name': 'Samsung Galaxy S24', 'description': 'Compact flagship with advanced camera', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000005/ecommerce/galaxys24.jpg'},
        {'name': 'Google Pixel 8 Pro', 'description': 'AI-powered camera with 7 years of updates', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000006/ecommerce/pixel8pro.jpg'},
        {'name': 'Google Pixel 8', 'description': 'Pure Android experience with Tensor G3', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000007/ecommerce/pixel8.jpg'},
        {'name': 'OnePlus 12', 'description': 'Fast charging flagship with Hasselblad camera', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000008/ecommerce/oneplus12.jpg'},
        {'name': 'Xiaomi 14', 'description': 'Leica camera partnership with Snapdragon 8 Gen 3', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000009/ecommerce/xiaomi14.jpg'},
    ]
    
    print(f"🚀 Ajout de {len(phone_products)} produits via l'API...")
    
    success_count = 0
    for i, product in enumerate(phone_products, 1):
        try:
            # Utiliser l'endpoint de création de produit
            response = requests.post(
                f"{API_BASE_URL}/product/create",
                data=product,
                timeout=10
            )
            
            if response.status_code == 200 or response.status_code == 201:
                success_count += 1
                print(f"✅ {i:2d}/10: {product['name'][:30]:<30} - Ajouté")
            else:
                print(f"❌ {i:2d}/10: {product['name'][:30]:<30} - Erreur {response.status_code}")
                
        except Exception as e:
            print(f"❌ {i:2d}/10: {product['name'][:30]:<30} - Exception: {str(e)[:50]}")
    
    print(f"\n🎉 Terminé! {success_count}/10 produits ajoutés avec succès.")
    return success_count

if __name__ == '__main__':
    populate_products_via_api()
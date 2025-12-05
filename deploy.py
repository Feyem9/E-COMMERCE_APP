#!/usr/bin/env python3
"""
Script d'initialisation pour Render - PostgreSQL
Ce script sera exécuté lors du déploiement sur Render
Utilise les URLs Cloudinary du compte df6hzqdjo
"""
import os
from flask import Flask

def deploy():
    """Exécuter les déploiements avec population de données."""
    
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
        
        print("✅ Tables créées! Suppression des anciens produits...")
        
        # TOUJOURS supprimer les anciens produits et les re-créer avec les bonnes URLs
        old_product_count = Products.query.count()
        print(f"📊 Anciens produits trouvés: {old_product_count}")
        
        if old_product_count > 0:
            print("🗑️  Suppression des anciens produits...")
            Products.query.delete()
            db.session.commit()
            print("✅ Anciens produits supprimés")
        
        if True:
            print("📱 Ajout des 50 produits smartphones...")
            
            # Liste des produits smartphones avec URLs Cloudinary correctes (df6hzqdjo)
            phone_products = [
                {'name': 'iPhone 15 Pro', 'description': 'Latest iPhone with titanium design and A17 Pro chip', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'iPhone 15', 'description': 'Powerful iPhone with Dynamic Island and USB-C', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'iPhone 14 Pro', 'description': 'Pro camera system with 48MP sensor', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Ultimate Android flagship with S Pen', 'current_price': 1299.99, 'discount_price': 1199.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Samsung Galaxy S24+', 'description': 'Large screen Android phone with AI features', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Samsung Galaxy S24', 'description': 'Compact flagship with advanced camera', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Google Pixel 8 Pro', 'description': 'AI-powered camera with 7 years of updates', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'Google Pixel 8', 'description': 'Pure Android experience with Tensor G3', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'OnePlus 12', 'description': 'Fast charging flagship with Hasselblad camera', 'current_price': 899.99, 'discount_price': 799.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/phone_camera.avif'},
                {'name': 'Xiaomi 14', 'description': 'Leica camera partnership with Snapdragon 8 Gen 3', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Huawei P60 Pro', 'description': 'XMAGE camera system with variable aperture', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712305/ecommerce/premium_photo-1678865183651-ef7d83d50b8f.avif'},
                {'name': 'Sony Xperia 1 V', 'description': 'Professional camera phone for creators', 'current_price': 1399.99, 'discount_price': 1299.99, 'quantity': 10, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712303/ecommerce/photo-1624259416658-35ccbf144757.avif'},
                {'name': 'Asus ROG Phone 8', 'description': 'Gaming phone with 165Hz display', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 12, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712300/ecommerce/photo-1598865776903-650a9302ccac.avif'},
                {'name': 'Nothing Phone (2a)', 'description': 'Unique design with Glyph interface', 'current_price': 399.99, 'discount_price': 349.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712299/ecommerce/photo-1587749090881-1ea18126ab3a.avif'},
                {'name': 'Motorola Edge 40 Pro', 'description': 'Premium Android with curved display', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712297/ecommerce/photo-1556742517-fde6c2abbe11.avif'},
                {'name': 'Oppo Find X7 Ultra', 'description': 'Quad camera system with Hasselblad tuning', 'current_price': 1299.99, 'discount_price': 1199.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/phone_camera.avif'},
                {'name': 'Vivo X100 Pro', 'description': 'ZEISS camera with professional video features', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/infinix_generic.jpg'},
                {'name': 'Realme GT 5', 'description': 'Performance flagship with ice-cooling', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Nokia X30', 'description': 'Durable phone with 5 years of updates', 'current_price': 499.99, 'discount_price': 449.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Fairphone 5', 'description': 'Ethical and repairable smartphone', 'current_price': 699.99, 'discount_price': 649.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'iPhone SE (3rd gen)', 'description': 'Affordable iPhone with A15 Bionic', 'current_price': 429.99, 'discount_price': 379.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'Samsung Galaxy A54', 'description': 'Mid-range Android with IP67 rating', 'current_price': 349.99, 'discount_price': 299.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Google Pixel 7a', 'description': 'Budget Pixel with Tensor G2', 'current_price': 499.99, 'discount_price': 449.99, 'quantity': 28, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'OnePlus 11', 'description': 'Fast charging with 100W SuperVOOC', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/phone_camera.avif'},
                {'name': 'Xiaomi 13', 'description': 'Leica optics with variable aperture', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Huawei Mate 50 Pro', 'description': 'XMAGE system with satellite connectivity', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/premium_photo-1679913792906-13ccc5c84d44.avif'},
                {'name': 'Sony Xperia 5 V', 'description': 'Compact flagship for photography', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 12, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712304/ecommerce/photo-1653630795384-fa8a46d8d382.avif'},
                {'name': 'Asus Zenfone 10', 'description': 'Compact Android with Snapdragon 8 Gen 2', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'Nothing Phone (2)', 'description': 'Transparent design with Android 13', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712299/ecommerce/photo-1578319439584-104c94d37305.avif'},
                {'name': 'Motorola Moto G84', 'description': 'Mid-range with 50MP camera', 'current_price': 299.99, 'discount_price': 249.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Oppo Reno 11', 'description': 'Selfie expert with 32MP front camera', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'Vivo V29', 'description': 'Beauty camera with 50MP sensor', 'current_price': 399.99, 'discount_price': 349.99, 'quantity': 28, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/infinix_generic.jpg'},
                {'name': 'Realme 11 Pro+', 'description': '100W charging with 200MP camera', 'current_price': 349.99, 'discount_price': 299.99, 'quantity': 32, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'Nokia G42', 'description': 'Budget phone with 3 years of updates', 'current_price': 199.99, 'discount_price': 149.99, 'quantity': 45, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Fairphone 4', 'description': 'Modular and sustainable design', 'current_price': 579.99, 'discount_price': 529.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'iPhone 13', 'description': 'Reliable iPhone with great value', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'},
                {'name': 'Samsung Galaxy A34', 'description': 'Affordable Android with 128GB storage', 'current_price': 299.99, 'discount_price': 249.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Google Pixel 7', 'description': 'Stock Android with excellent camera', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'OnePlus Nord CE 3', 'description': 'Budget flagship with 80W charging', 'current_price': 329.99, 'discount_price': 279.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/phone_camera.avif'},
                {'name': 'Xiaomi Redmi Note 13', 'description': 'Value for money with 108MP camera', 'current_price': 249.99, 'discount_price': 199.99, 'quantity': 50, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/smartphone_generic.avif'},
                {'name': 'Huawei Nova 11', 'description': 'Stylish phone with ring light camera', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712304/ecommerce/premium_photo-1668418188837-d40b734ed6d2.avif'},
                {'name': 'Sony Xperia 10 V', 'description': 'Mid-range with 21:9 display', 'current_price': 449.99, 'discount_price': 399.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712302/ecommerce/photo-1612442443556-09b5b309e637.avif'},
                {'name': 'Asus ROG Phone 7', 'description': 'Gaming beast with AirTriggers', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712301/ecommerce/photo-1607252650355-f7fd0460ccdb.avif'},
                {'name': 'Nothing Phone (1)', 'description': 'Innovative design with Android 12', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712298/ecommerce/photo-1572569979132-b4f10c9ec185.avif'},
                {'name': 'Motorola Edge 30 Ultra', 'description': 'Premium camera with 200MP sensor', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Oppo A98', 'description': 'Budget option with 64MP camera', 'current_price': 249.99, 'discount_price': 199.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif'},
                {'name': 'Vivo Y78', 'description': 'Entry-level with 50MP camera', 'current_price': 199.99, 'discount_price': 149.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/infinix_generic.jpg'},
                {'name': 'Realme C55', 'description': 'Basic phone with long battery life', 'current_price': 149.99, 'discount_price': 119.99, 'quantity': 55, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif'},
                {'name': 'Nokia C32', 'description': 'Durable budget phone', 'current_price': 129.99, 'discount_price': 99.99, 'quantity': 60, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif'},
                {'name': 'Fairphone 3+', 'description': 'Repairable and upgradable', 'current_price': 449.99, 'discount_price': 399.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg'}
            ]
            
            success_count = 0
            try:
                for product_data in phone_products:
                    product = Products(**product_data)
                    db.session.add(product)
                    success_count += 1
                
                db.session.commit()
                print(f"✅ {success_count} produits ajoutés avec succès!")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Erreur lors de l'ajout des produits: {e}")
        
        print("🎉 Déploiement terminé!")
        print("  - Tables créées")
        print(f"  - {Products.query.count()} produits dans la base")

if __name__ == '__main__':
    deploy()

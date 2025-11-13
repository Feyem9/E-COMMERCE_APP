from app import app, db
from models.product_model import Products
import os

def populate_products():
    """Peupler la base de données avec des produits de téléphones"""
    
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
        {'name': 'Huawei P60 Pro', 'description': 'XMAGE camera system with variable aperture', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000010/ecommerce/huaweip60pro.jpg'},
        {'name': 'Sony Xperia 1 V', 'description': 'Professional camera phone for creators', 'current_price': 1399.99, 'discount_price': 1299.99, 'quantity': 10, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000011/ecommerce/xperia1v.jpg'},
        {'name': 'Asus ROG Phone 8', 'description': 'Gaming phone with 165Hz display', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 12, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000012/ecommerce/rogphone8.jpg'},
        {'name': 'Nothing Phone (2a)', 'description': 'Unique design with Glyph interface', 'current_price': 399.99, 'discount_price': 349.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000013/ecommerce/nothingphone2a.jpg'},
        {'name': 'Motorola Edge 40 Pro', 'description': 'Premium Android with curved display', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000014/ecommerce/edge40pro.jpg'},
        {'name': 'Oppo Find X7 Ultra', 'description': 'Quad camera system with Hasselblad tuning', 'current_price': 1299.99, 'discount_price': 1199.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000015/ecommerce/findx7ultra.jpg'},
        {'name': 'Vivo X100 Pro', 'description': 'ZEISS camera with professional video features', 'current_price': 1199.99, 'discount_price': 1099.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000016/ecommerce/vivox100pro.jpg'},
        {'name': 'Realme GT 5', 'description': 'Performance flagship with ice-cooling', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000017/ecommerce/realmegt5.jpg'},
        {'name': 'Nokia X30', 'description': 'Durable phone with 5 years of updates', 'current_price': 499.99, 'discount_price': 449.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000018/ecommerce/nokiax30.jpg'},
        {'name': 'Fairphone 5', 'description': 'Ethical and repairable smartphone', 'current_price': 699.99, 'discount_price': 649.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000019/ecommerce/fairphone5.jpg'},
        {'name': 'iPhone SE (3rd gen)', 'description': 'Affordable iPhone with A15 Bionic', 'current_price': 429.99, 'discount_price': 379.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000020/ecommerce/iphonese.jpg'},
        {'name': 'Samsung Galaxy A54', 'description': 'Mid-range Android with IP67 rating', 'current_price': 349.99, 'discount_price': 299.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000021/ecommerce/galaxya54.jpg'},
        {'name': 'Google Pixel 7a', 'description': 'Budget Pixel with Tensor G2', 'current_price': 499.99, 'discount_price': 449.99, 'quantity': 28, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000022/ecommerce/pixel7a.jpg'},
        {'name': 'OnePlus 11', 'description': 'Fast charging with 100W SuperVOOC', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000023/ecommerce/oneplus11.jpg'},
        {'name': 'Xiaomi 13', 'description': 'Leica optics with variable aperture', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000024/ecommerce/xiaomi13.jpg'},
        {'name': 'Huawei Mate 50 Pro', 'description': 'XMAGE system with satellite connectivity', 'current_price': 1099.99, 'discount_price': 999.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000025/ecommerce/mate50pro.jpg'},
        {'name': 'Sony Xperia 5 V', 'description': 'Compact flagship for photography', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 12, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000026/ecommerce/xperia5v.jpg'},
        {'name': 'Asus Zenfone 10', 'description': 'Compact Android with Snapdragon 8 Gen 2', 'current_price': 799.99, 'discount_price': 699.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000027/ecommerce/zenfone10.jpg'},
        {'name': 'Nothing Phone (2)', 'description': 'Transparent design with Android 13', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000028/ecommerce/nothingphone2.jpg'},
        {'name': 'Motorola Moto G84', 'description': 'Mid-range with 50MP camera', 'current_price': 299.99, 'discount_price': 249.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000029/ecommerce/motog84.jpg'},
        {'name': 'Oppo Reno 11', 'description': 'Selfie expert with 32MP front camera', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000030/ecommerce/reno11.jpg'},
        {'name': 'Vivo V29', 'description': 'Beauty camera with 50MP sensor', 'current_price': 399.99, 'discount_price': 349.99, 'quantity': 28, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000031/ecommerce/vivov29.jpg'},
        {'name': 'Realme 11 Pro+', 'description': '100W charging with 200MP camera', 'current_price': 349.99, 'discount_price': 299.99, 'quantity': 32, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000032/ecommerce/realme11proplus.jpg'},
        {'name': 'Nokia G42', 'description': 'Budget phone with 3 years of updates', 'current_price': 199.99, 'discount_price': 149.99, 'quantity': 45, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000033/ecommerce/nokiag42.jpg'},
        {'name': 'Fairphone 4', 'description': 'Modular and sustainable design', 'current_price': 579.99, 'discount_price': 529.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000034/ecommerce/fairphone4.jpg'},
        {'name': 'iPhone 13', 'description': 'Reliable iPhone with great value', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000035/ecommerce/iphone13.jpg'},
        {'name': 'Samsung Galaxy A34', 'description': 'Affordable Android with 128GB storage', 'current_price': 299.99, 'discount_price': 249.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000036/ecommerce/galaxya34.jpg'},
        {'name': 'Google Pixel 7', 'description': 'Stock Android with excellent camera', 'current_price': 599.99, 'discount_price': 499.99, 'quantity': 22, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000037/ecommerce/pixel7.jpg'},
        {'name': 'OnePlus Nord CE 3', 'description': 'Budget flagship with 80W charging', 'current_price': 329.99, 'discount_price': 279.99, 'quantity': 30, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000038/ecommerce/nordce3.jpg'},
        {'name': 'Xiaomi Redmi Note 13', 'description': 'Value for money with 108MP camera', 'current_price': 249.99, 'discount_price': 199.99, 'quantity': 50, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000039/ecommerce/redminote13.jpg'},
        {'name': 'Huawei Nova 11', 'description': 'Stylish phone with ring light camera', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 25, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000040/ecommerce/nova11.jpg'},
        {'name': 'Sony Xperia 10 V', 'description': 'Mid-range with 21:9 display', 'current_price': 449.99, 'discount_price': 399.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000041/ecommerce/xperia10v.jpg'},
        {'name': 'Asus ROG Phone 7', 'description': 'Gaming beast with AirTriggers', 'current_price': 999.99, 'discount_price': 899.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000042/ecommerce/rogphone7.jpg'},
        {'name': 'Nothing Phone (1)', 'description': 'Innovative design with Android 12', 'current_price': 499.99, 'discount_price': 399.99, 'quantity': 20, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000043/ecommerce/nothingphone1.jpg'},
        {'name': 'Motorola Edge 30 Ultra', 'description': 'Premium camera with 200MP sensor', 'current_price': 699.99, 'discount_price': 599.99, 'quantity': 18, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000044/ecommerce/edge30ultra.jpg'},
        {'name': 'Oppo A98', 'description': 'Budget option with 64MP camera', 'current_price': 249.99, 'discount_price': 199.99, 'quantity': 35, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000045/ecommerce/oppoa98.jpg'},
        {'name': 'Vivo Y78', 'description': 'Entry-level with 50MP camera', 'current_price': 199.99, 'discount_price': 149.99, 'quantity': 40, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000046/ecommerce/vivoy78.jpg'},
        {'name': 'Realme C55', 'description': 'Basic phone with long battery life', 'current_price': 149.99, 'discount_price': 119.99, 'quantity': 55, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000047/ecommerce/realmec55.jpg'},
        {'name': 'Nokia C32', 'description': 'Durable budget phone', 'current_price': 129.99, 'discount_price': 99.99, 'quantity': 60, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000048/ecommerce/nokiac32.jpg'},
        {'name': 'Fairphone 3+', 'description': 'Repairable and upgradable', 'current_price': 449.99, 'discount_price': 399.99, 'quantity': 15, 'picture': 'https://res.cloudinary.com/dzqbzqgjw/image/upload/v1733000049/ecommerce/fairphone3plus.jpg'}
    ]

    with app.app_context():
        # Vérifier si des produits existent déjà
        existing_count = Products.query.count()
        print(f"📊 Produits existants: {existing_count}")
        
        if existing_count > 0:
            print("⚠️  La base contient déjà des produits. Voulez-vous les remplacer ?")
            # Pour ce script, on va ajouter sans supprimer
            print("➕ Ajout des nouveaux produits...")
        
        success_count = 0
        for product_data in phone_products:
            try:
                # Vérifier si le produit existe déjà
                existing = Products.query.filter_by(name=product_data['name']).first()
                if not existing:
                    product = Products(**product_data)
                    db.session.add(product)
                    success_count += 1
                    print(f"✅ Ajouté: {product_data['name']}")
                else:
                    print(f"⏭️  Existe déjà: {product_data['name']}")
            except Exception as e:
                print(f"❌ Erreur avec {product_data['name']}: {str(e)}")
        
        try:
            db.session.commit()
            print(f"\n🎉 Succès! {success_count} nouveaux produits ajoutés sur {len(phone_products)} total.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la sauvegarde: {e}")

if __name__ == '__main__':
    populate_products()

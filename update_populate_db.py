#!/usr/bin/env python3
"""
Script pour mettre à jour populate_db.py avec les vraies URLs Cloudinary
"""

import re

# Mapping des images principales utilisées dans populate_db
PRODUCT_IMAGE_MAP = {
    'iphone15pro': 'iphone_generic',
    'iphone15': 'iphone_generic',
    'iphone14pro': 'iphone_generic',
    'iphone14': 'iphone_generic',
    'iphonese': 'iphone_generic',
    'iphone13': 'iphone_generic',
    
    'galaxys24ultra': 'samsung_generic',
    'galaxys24plus': 'samsung_generic',
    'galaxys24': 'samsung_generic',
    'galaxys23': 'samsung_generic',
    'galaxya54': 'samsung_generic',
    'galaxya34': 'samsung_generic',
    
    'pixel8pro': 'phone_display',
    'pixel8': 'phone_display',
    'pixel7a': 'phone_display',
    'pixel7': 'phone_display',
    
    'oneplus12': 'phone_camera',
    'oneplus11': 'phone_camera',
    
    'xiaomi14': 'phone_tech',
    'xiaomi13': 'phone_tech',
    
    'huaweip60pro': 'premium_photo-1678865183651-ef7d83d50b8f',
    'mate50pro': 'premium_photo-1679913792906-13ccc5c84d44',
    'nova11': 'premium_photo-1668418188837-d40b734ed6d2',
    
    'xperia1v': 'photo-1624259416658-35ccbf144757',
    'xperia5v': 'photo-1653630795384-fa8a46d8d382',
    'xperia10v': 'photo-1612442443556-09b5b309e637',
    
    'rogphone8': 'photo-1598865776903-650a9302ccac',
    'rogphone7': 'photo-1607252650355-f7fd0460ccdb',
    
    'nothingphone2a': 'photo-1587749090881-1ea18126ab3a',
    'nothingphone2': 'photo-1578319439584-104c94d37305',
    'nothingphone1': 'photo-1572569979132-b4f10c9ec185',
    
    'edge40pro': 'photo-1556742517-fde6c2abbe11',
    'edge30ultra': 'photo-1546868871-7041f2a55e12',
    
    'findx7ultra': 'photo-1546054454-aa26e2b734c7',
    'reno11': 'photo-1520189123429-6a76abfe7906',
    
    'vivox100pro': 'infinix_generic',
    'vivov29': 'infinix_generic',
    'vivoy78': 'infinix_generic',
    
    'zenfone10': 'iphone_generic',
    
    'realmegt5': 'samsung_generic',
    'realme11proplus': 'phone_display',
    'realmec55': 'phone_camera',
    
    'nokiax30': 'phone_tech',
    'nokiag42': 'phone_tech',
    'nokiac32': 'phone_tech',
    
    'fairphone5': 'iphone_generic',
    'fairphone4': 'iphone_generic',
    'fairphone3plus': 'iphone_generic',
    
    'motog84': 'samsung_generic',
    'oppoa98': 'phone_display',
}

# URLs Cloudinary générées
CLOUDINARY_URLS = {
    'iphone_generic': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/iphone_generic.jpg',
    'samsung_generic': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/samsung_generic.avif',
    'phone_display': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif',
    'phone_camera': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/phone_camera.avif',
    'phone_tech': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/phone_tech.avif',
    'premium_photo-1668418188837-d40b734ed6d2': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712304/ecommerce/premium_photo-1668418188837-d40b734ed6d2.avif',
    'premium_photo-1678865183651-ef7d83d50b8f': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712305/ecommerce/premium_photo-1678865183651-ef7d83d50b8f.avif',
    'premium_photo-1679913792906-13ccc5c84d44': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712306/ecommerce/premium_photo-1679913792906-13ccc5c84d44.avif',
    'photo-1624259416658-35ccbf144757': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712303/ecommerce/photo-1624259416658-35ccbf144757.avif',
    'photo-1653630795384-fa8a46d8d382': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712304/ecommerce/photo-1653630795384-fa8a46d8d382.avif',
    'photo-1612442443556-09b5b309e637': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712302/ecommerce/photo-1612442443556-09b5b309e637.avif',
    'photo-1598865776903-650a9302ccac': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712300/ecommerce/photo-1598865776903-650a9302ccac.avif',
    'photo-1607252650355-f7fd0460ccdb': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712301/ecommerce/photo-1607252650355-f7fd0460ccdb.avif',
    'photo-1587749090881-1ea18126ab3a': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712299/ecommerce/photo-1587749090881-1ea18126ab3a.avif',
    'photo-1578319439584-104c94d37305': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712299/ecommerce/photo-1578319439584-104c94d37305.avif',
    'photo-1572569979132-b4f10c9ec185': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712298/ecommerce/photo-1572569979132-b4f10c9ec185.avif',
    'photo-1556742517-fde6c2abbe11': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712297/ecommerce/photo-1556742517-fde6c2abbe11.avif',
    'photo-1546868871-7041f2a55e12': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712296/ecommerce/photo-1546868871-7041f2a55e12.avif',
    'photo-1546054454-aa26e2b734c7': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712295/ecommerce/photo-1546054454-aa26e2b734c7.avif',
    'photo-1520189123429-6a76abfe7906': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712294/ecommerce/phone_display.avif',
    'infinix_generic': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712292/ecommerce/infinix_generic.jpg',
    'smartphone_generic': 'https://res.cloudinary.com/df6hzqdjo/image/upload/v1764712307/ecommerce/smartphone_generic.avif',
}

def update_populate_db():
    """Mets à jour populate_db.py avec les vraies URLs"""
    
    file_path = 'populate_db.py'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated_count = 0
        
        # Pour chaque produit, remplacer l'URL fictive par la vraie
        for product_id, image_name in PRODUCT_IMAGE_MAP.items():
            # Pattern pour trouver la ligne du produit
            pattern = rf"({product_id}\.jpg['\"])"
            cloudinary_url = CLOUDINARY_URLS.get(image_name, CLOUDINARY_URLS['iphone_generic'])
            replacement = f"{cloudinary_url}'"
            
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                updated_count += 1
        
        # Vérifier si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ populate_db.py mis à jour!")
            print(f"   {updated_count} URLs mises à jour")
            return True
        else:
            print(f"⚠️  Aucune mise à jour nécessaire")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == '__main__':
    print("🔄 Mise à jour de populate_db.py avec les vraies URLs Cloudinary...\n")
    update_populate_db()

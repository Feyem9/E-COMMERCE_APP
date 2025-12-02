#!/usr/bin/env python3
"""
Script pour uploader les images locales vers Cloudinary
Utilise les credentials de cloudinary_config.py
"""

import os
import glob
import sys
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configuration Cloudinary (utilise les mêmes que cloudinary_config.py)
CLOUD_NAME = "df6hzqdjo"
API_KEY = "398615211289795"
API_SECRET = "N_wY-Pd-4nLaEtL9Ofy8KtEsLX0"

# Dossier contenant les images locales
LOCAL_IMAGES_DIR = "/home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP/public"

# Dossier de destination dans Cloudinary
CLOUDINARY_FOLDER = "ecommerce"

# Extensions d'images supportées
IMAGE_EXTENSIONS = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.avif', '*.gif')

# Map de correspondance entre fichiers locaux et noms de produits
IMAGE_NAME_MAP = {
    'iphone.jpeg': 'iphone_generic',
    'samsung.avif': 'samsung_generic',
    'smart.avif': 'smartphone_generic',
    'infinix.jpeg': 'infinix_generic',
    'photo-1520189123429-6a76abfe7906.avif': 'phone_display',
    'photo-1546054454-aa26e2b734c7.avif': 'phone_camera',
    'photo-1546868871-7041f2a55e12.avif': 'phone_tech',
}

def configure_cloudinary():
    """Configure les paramètres Cloudinary"""
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    print(f"✅ Cloudinary configuré pour: {CLOUD_NAME}")

def get_local_images():
    """Récupère la liste des images locales"""
    images = []
    for ext in IMAGE_EXTENSIONS:
        pattern = os.path.join(LOCAL_IMAGES_DIR, ext)
        images.extend(glob.glob(pattern))
    return sorted(images)

def upload_image_to_cloudinary(local_path, folder):
    """Uploade une image vers Cloudinary"""
    try:
        file_name = os.path.basename(local_path)
        
        # Utilise le nom mappé si disponible, sinon le nom du fichier
        public_id = IMAGE_NAME_MAP.get(file_name, os.path.splitext(file_name)[0])
        
        print(f"⏳ Uploading: {file_name}...", end=" ", flush=True)
        
        result = cloudinary.uploader.upload(
            local_path,
            folder=folder,
            public_id=public_id,
            overwrite=True,
            resource_type="auto"
        )
        
        print(f"✅")
        return {
            'file': file_name,
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Script d'upload d'images vers Cloudinary\n")
    
    # Vérifier que le dossier existe
    if not os.path.exists(LOCAL_IMAGES_DIR):
        print(f"❌ Erreur: Dossier {LOCAL_IMAGES_DIR} introuvable")
        print(f"   Cherchant dans: {os.path.abspath(LOCAL_IMAGES_DIR)}")
        return
    
    # Récupérer les images
    images = get_local_images()
    if not images:
        print(f"❌ Aucune image trouvée dans {LOCAL_IMAGES_DIR}")
        return
    
    print(f"📦 {len(images)} images trouvées\n")
    for img in images[:5]:  # Affiche les 5 premières
        print(f"   - {os.path.basename(img)}")
    if len(images) > 5:
        print(f"   ... et {len(images) - 5} autres\n")
    
    # Configurer Cloudinary
    configure_cloudinary()
    print()
    
    # Demander confirmation
    response = input("Voulez-vous continuer avec l'upload? (oui/non): ").lower()
    if response not in ['oui', 'yes', 'o', 'y']:
        print("❌ Upload annulé.")
        return
    
    print()
    
    # Uploader chaque image
    results = []
    failed = []
    
    for i, local_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] ", end="")
        result = upload_image_to_cloudinary(local_path, CLOUDINARY_FOLDER)
        if result:
            results.append(result)
        else:
            failed.append(os.path.basename(local_path))
    
    print(f"\n{'='*60}")
    print(f"✅ Upload terminé!")
    print(f"{'='*60}\n")
    
    # Résumé
    print(f"📊 Résumé:")
    print(f"   ✅ Succès: {len(results)}")
    print(f"   ❌ Erreurs: {len(failed)}")
    print()
    
    # Générer la liste des URLs pour populate_db.py
    print("📋 URLs pour populate_db.py:\n")
    print("Copie ces URLs et mets-les à jour dans populate_db.py:\n")
    
    for result in results:
        print(f"'{result['file']}' → {result['url']}")
    
    if failed:
        print(f"\n⚠️  Images en erreur: {', '.join(failed)}")
    
    print(f"\n💾 Les images sont maintenant sur Cloudinary!")
    print(f"   Cloud: {CLOUD_NAME}")
    print(f"   Dossier: {CLOUDINARY_FOLDER}/")

if __name__ == "__main__":
    main()

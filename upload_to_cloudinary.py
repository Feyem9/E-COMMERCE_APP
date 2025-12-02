#!/usr/bin/env python3
"""
Script pour uploader les images locales vers Cloudinary
"""

import os
import glob
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configuration Cloudinary
CLOUD_NAME = "dzqbzqgjw"
# Tu dois générer une API Key et Secret depuis https://cloudinary.com/console
API_KEY = "YOUR_API_KEY"  # À remplacer
API_SECRET = "YOUR_API_SECRET"  # À remplacer

# Dossier contenant les images locales
LOCAL_IMAGES_DIR = "../../frontend/E-COMMERCE_APP/public"

# Dossier de destination dans Cloudinary
CLOUDINARY_FOLDER = "ecommerce"

# Extensions d'images supportées
IMAGE_EXTENSIONS = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.avif', '*.gif')

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
    return images

def upload_image_to_cloudinary(local_path, folder):
    """Uploade une image vers Cloudinary"""
    try:
        file_name = os.path.basename(local_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        print(f"Uploading: {file_name}...", end=" ")
        
        result = cloudinary.uploader.upload(
            local_path,
            folder=folder,
            public_id=file_name_without_ext,
            overwrite=True,
            resource_type="auto"
        )
        
        print(f"✅ Success")
        print(f"   URL: {result['secure_url']}")
        return result['secure_url']
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Script d'upload d'images vers Cloudinary\n")
    
    # Vérifier que le dossier existe
    if not os.path.exists(LOCAL_IMAGES_DIR):
        print(f"❌ Erreur: Dossier {LOCAL_IMAGES_DIR} introuvable")
        return
    
    # Récupérer les images
    images = get_local_images()
    if not images:
        print(f"❌ Aucune image trouvée dans {LOCAL_IMAGES_DIR}")
        return
    
    print(f"📦 {len(images)} images trouvées\n")
    
    # Configurer Cloudinary
    configure_cloudinary()
    print()
    
    # Uploader chaque image
    urls_map = {}
    for local_path in images:
        url = upload_image_to_cloudinary(local_path, CLOUDINARY_FOLDER)
        if url:
            file_name = os.path.basename(local_path)
            urls_map[file_name] = url
    
    print(f"\n✅ Upload terminé!\n")
    
    # Générer la liste des URLs
    print("📋 Voici les URLs pour mettre à jour populate_db.py:\n")
    for file_name, url in urls_map.items():
        print(f"'{file_name}': '{url}'")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script d'initialisation pour Render - PostgreSQL
Ce script sera exécuté lors du déploiement sur Render
"""
import os
from flask import Flask
from flask_migrate import upgrade

def deploy():
    """Exécuter les déploiements."""
    
    # Importer l'app
    from app import app
    
    with app.app_context():
        # Migrer la base de données vers la dernière révision
        upgrade()
        
        print("✅ Déploiement terminé!")

if __name__ == '__main__':
    deploy()
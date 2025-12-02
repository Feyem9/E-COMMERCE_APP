#!/bin/bash
set -o errexit

echo "🔧 Démarrage du script de construction..."

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Exécuter les migrations Alembic
echo "🗄️  Exécution des migrations Alembic..."
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/backend/E-COMMERCE_APP
flask db upgrade || echo "⚠️  Les migrations n'ont pas pu être exécutées automatiquement"

# Peupler la base de données
echo "🌱 Peuplement de la base de données..."
python3 populate_db.py

echo "✅ Script de construction terminé!"

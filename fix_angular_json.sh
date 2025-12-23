#!/bin/bash
# Fix angular.json assets

cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Backup
cp angular.json angular.json.bak

# Python pour fix propre
python3 << 'EOF'
import json

with open('angular.json', 'r') as f:
    config = json.load(f)

# Ajouter src/assets 
assets = config['projects']['market']['architect']['build']['options']['assets']

# Vérifier si src/assets n'est pas déjà là
has_src_assets = any(
    isinstance(a, dict) and a.get('input') == 'src/assets' 
    for a in assets
)

if not has_src_assets:
    assets.append({
        "glob": "**/*",
        "input": "src/assets",
        "output": "/assets"
    })
    print("✅ src/assets ajouté")
else:
    print("✅ src/assets déjà présent")

with open('angular.json', 'w') as f:
    json.dump(config, f, indent=2)

EOF

echo "✅ angular.json mis à jour"

# 🚀 GitHub Actions CI/CD - Démarrage Rapide

**Temps estimé**: 10 minutes  
**Difficulté**: ⭐⭐☆☆☆ (Facile)

---

## ⚡ Installation en 3 Étapes

### **Étape 1: Vérifier les fichiers** (1 min)

Les fichiers suivants ont été créés:
```
.github/
├── workflows/
│   ├── ci-simple.yml        ← Configuration simple ⭐ RECOMMANDÉ
│   └── ci.yml               ← Configuration complète
└── GITHUB_ACTIONS_GUIDE.md  ← Guide complet
```

Vérifiez qu'ils existent:
```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
ls -la .github/workflows/
```

---

### **Étape 2: Push vers GitHub** (2 min)

```bash
# Ajouter les fichiers
git add .github/

# Commit
git commit -m "ci: Add GitHub Actions CI/CD pipeline"

# Push (remplacer 'front-end' par votre branche si différent)
git push origin front-end
```

---

### **Étape 3: Vérifier sur GitHub** (1 min)

1. Aller sur: `https://github.com/YOUR_USERNAME/YOUR_REPO`
2. Cliquer sur l'onglet **"Actions"**
3. Vous devriez voir le workflow en cours d'exécution ! ✅

**C'est tout pour la configuration de base !** 🎉

---

## 🔐 Configuration Avancée (Déploiement Automatique)

Pour activer le **déploiement automatique vers Vercel**, suivez ces étapes:

### **1. Obtenir les secrets Vercel** (3 min)

<function_calls>
<invoke name="write_to_file">
<parameter name="CodeContent">#!/bin/bash

# Script pour récupérer les secrets Vercel
# Usage: ./get-vercel-secrets.sh

echo "════════════════════════════════════════════════════════════════"
echo "  🔐 Récupération des Secrets Vercel pour GitHub Actions"
echo "════════════════════════════════════════════════════════════════"
echo ""

PROJECT_DIR="/home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP"

# Vérifier si Vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI n'est pas installé."
    echo ""
    echo "📦 Installation:"
    echo "   npm install -g vercel"
    echo ""
    exit 1
fi

echo "✅ Vercel CLI détecté"
echo ""

# Vérifier si le projet est lié
if [ ! -f "$PROJECT_DIR/.vercel/project.json" ]; then
    echo "⚠️  Projet non lié à Vercel."
    echo ""
    echo "🔗 Pour lier le projet:"
    echo "   cd $PROJECT_DIR"
    echo "   vercel link"
    echo ""
    read -p "Voulez-vous lier le projet maintenant? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$PROJECT_DIR"
        vercel link
    else
        exit 1
    fi
fi

echo "════════════════════════════════════════════════════════════════"
echo "  📋 VOS SECRETS VERCEL"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Lire le fichier project.json
if [ -f "$PROJECT_DIR/.vercel/project.json" ]; then
    echo "📂 Lecture de .vercel/project.json..."
    echo ""
    
    ORG_ID=$(cat "$PROJECT_DIR/.vercel/project.json" | grep -o '"orgId": "[^"]*' | cut -d'"' -f4)
    PROJECT_ID=$(cat "$PROJECT_DIR/.vercel/project.json" | grep -o '"projectId": "[^"]*' | cut -d'"' -f4)
    
    echo "1️⃣  VERCEL_ORG_ID:"
    echo "   $ORG_ID"
    echo ""
    
    echo "2️⃣  VERCEL_PROJECT_ID:"
    echo "   $PROJECT_ID"
    echo ""
fi

echo "3️⃣  VERCEL_TOKEN:"
echo "   ⚠️  Ce secret doit être généré manuellement"
echo ""
echo "   📍 Pour obtenir votre token:"
echo "      1. Aller sur: https://vercel.com/account/tokens"
echo "      2. Cliquer sur 'Create Token'"
echo "      3. Donner un nom: 'GitHub Actions CI/CD'"
echo "      4. Copier le token (commence par 'vercel_...')"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "  📝 ÉTAPES SUIVANTES"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "1. Copier les valeurs ci-dessus"
echo ""
echo "2. Aller sur GitHub:"
echo "   https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions"
echo ""
echo "3. Ajouter ces 3 secrets:"
echo "   • VERCEL_TOKEN"
echo "   • VERCEL_ORG_ID"
echo "   • VERCEL_PROJECT_ID"
echo ""
echo "4. Push votre code vers la branche 'main' pour déclencher le déploiement"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

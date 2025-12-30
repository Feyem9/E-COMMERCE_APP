#!/bin/bash

# Script de déploiement staging rapide
# Usage: ./deploy-staging.sh

echo "════════════════════════════════════════════════════════════════"
echo "  🚀 Déploiement Staging - E-Commerce App"
echo "════════════════════════════════════════════════════════════════"
echo ""

PROJECT_DIR="/home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP"
cd "$PROJECT_DIR"

# Vérifier qu'on est dans le bon dossier
if [ ! -f "package.json" ]; then
    echo "❌ Erreur: package.json not found"
    echo "   Assurez-vous d'être dans le bon dossier"
    exit 1
fi

echo "📂 Dossier: $PROJECT_DIR"
echo ""

# Vérifier le statut Git
echo "📊 Statut Git:"
git status --short
echo ""

# Proposer les options
echo "═══════════════════════════════════════════════════════════════"
echo "  🎯 OPTIONS DE DÉPLOIEMENT STAGING"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1) 🚀 Déploiement rapide (Vercel CLI)"
echo "   → Déploie immédiatement sur staging"
echo "   → Temps: ~2 minutes"
echo ""
echo "2) 📊 Créer branche staging + push"
echo "   → Crée branche staging"
echo "   → Push vers GitHub"
echo "   → Vercel déploie automatiquement"
echo "   → Temps: ~5 minutes"
echo ""
echo "3) ℹ️  Afficher les instructions"
echo ""
echo "4) ❌ Annuler"
echo ""
read -p "Votre choix (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Déploiement rapide avec Vercel CLI..."
        echo ""
        
        # Vérifier si Vercel CLI est installé
        if ! command -v vercel &> /dev/null; then
            echo "📦 Installation de Vercel CLI..."
            npm install -g vercel
        fi
        
        echo "🔐 Login Vercel (si nécessaire)..."
        vercel whoami || vercel login
        
        echo ""
        echo "🏗️  Déploiement en cours..."
        vercel --target staging
        
        echo ""
        echo "✅ Déploiement terminé!"
        echo "🔗 Vérifiez l'URL dans la sortie ci-dessus"
        ;;
        
    2)
        echo ""
        echo "📊 Création de la branche staging..."
        
        # Sauvegarder la branche actuelle
        CURRENT_BRANCH=$(git branch --show-current)
        echo "   Branche actuelle: $CURRENT_BRANCH"
        
        # Créer ou checkout staging
        if git show-ref --verify --quiet refs/heads/staging; then
            echo "   ✅ Branche staging existe déjà"
            git checkout staging
        else
            echo "   🆕 Création de la branche staging"
            git checkout -b staging
        fi
        
        # Ajouter les changements
        echo ""
        echo "📦 Ajout des fichiers..."
        git add .github/
        
        # Commit
        echo ""
        read -p "📝 Message de commit [ci: Add staging deployment]: " commit_msg
        commit_msg=${commit_msg:-"ci: Add staging deployment"}
        git commit -m "$commit_msg" || echo "Rien à commiter"
        
        # Push
        echo ""
        echo "⬆️  Push vers GitHub..."
        git push origin staging
        
        echo ""
        echo "════════════════════════════════════════════════════════════"
        echo "  ✅ SUCCÈS!"
        echo "════════════════════════════════════════════════════════════"
        echo ""
        echo "🎉 Branche staging créée et push effectué!"
        echo ""
        echo "📍 Prochaines étapes:"
        echo "   1. Aller sur https://vercel.com/"
        echo "   2. Voir votre projet E-COMMERCE_APP"
        echo "   3. Onglet 'Deployments'"
        echo "   4. Trouver le deployment de la branche 'staging'"
        echo "   5. Cliquer pour voir l'URL!"
        echo ""
        echo "🔗 L'URL sera du type:"
        echo "   https://market-jet-staging-xxxxx.vercel.app"
        echo ""
        ;;
        
    3)
        echo ""
        echo "════════════════════════════════════════════════════════════"
        echo "  ℹ️  INSTRUCTIONS MANUELLES"
        echo "════════════════════════════════════════════════════════════"
        echo ""
        echo "Option A - Via Vercel CLI (Rapide):"
        echo "  1. npm install -g vercel"
        echo "  2. vercel login"
        echo "  3. vercel --target staging"
        echo ""
        echo "Option B - Via Git (Automatique):"
        echo "  1. git checkout -b staging"
        echo "  2. git add .github/"
        echo "  3. git commit -m 'ci: Add staging'"
        echo "  4. git push origin staging"
        echo "  5. Vercel déploie automatiquement!"
        echo ""
        echo "Option C - Via GitHub Actions:"
        echo "  1. Push vers branche 'staging'"
        echo "  2. Workflow deploy-staging.yml se déclenche"
        echo "  3. Déploiement automatique"
        echo ""
        ;;
        
    4)
        echo ""
        echo "❌ Annulé."
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ Choix invalide."
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════"

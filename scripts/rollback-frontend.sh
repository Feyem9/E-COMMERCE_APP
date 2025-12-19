#!/bin/bash

# ========================================
# Script de Rollback Frontend (Vercel)
# Date: 19 Décembre 2025
# ========================================

echo "════════════════════════════════════════════════════════════════"
echo "  🔄 ROLLBACK FRONTEND (Vercel)"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Vérifier si Vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI n'est pas installé"
    echo ""
    echo "Installation rapide:"
    echo "  npm install -g vercel"
    echo ""
    echo "OU faire le rollback manuellement:"
    echo "  1. Aller sur https://vercel.com/"
    echo "  2. Projet → Deployments"
    echo "  3. Choisir le deployment stable"
    echo "  4. Cliquer sur '...' → 'Promote to Production'"
    echo ""
    exit 1
fi

echo "📋 Liste des derniers déploiements:"
echo ""
vercel list --scope production

echo ""
echo "════════════════════════════════════════════════════════════════"
read -p "Entrer l'URL ou ID du deployment à restaurer: " DEPLOY_ID

if [ -z "$DEPLOY_ID" ]; then
    echo "❌ Aucun ID fourni. Annulation."
    exit 1
fi

echo ""
echo "🔄 Promotion du deployment $DEPLOY_ID en production..."
echo ""

# Promouvoir le deployment
vercel promote "$DEPLOY_ID" --scope production

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  ✅ ROLLBACK RÉUSSI !"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 Vérifier: https://market-jet.vercel.app"
    echo ""
    echo "⏱️  La propagation peut prendre 1-2 minutes"
    echo ""
else
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  ❌ ROLLBACK ÉCHOUÉ"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "Essayer le rollback manuel:"
    echo "  https://vercel.com/dashboard"
    echo ""
    exit 1
fi

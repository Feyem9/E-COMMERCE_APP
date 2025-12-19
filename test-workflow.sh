#!/bin/bash

# Script pour tester le workflow après configuration des secrets
# Date: 19 Décembre 2025

echo "════════════════════════════════════════════════════════════════"
echo "  🚀 Test du Workflow avec Secrets Vercel"
echo "════════════════════════════════════════════════════════════════"
echo ""

cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

echo "📍 Branche actuelle:"
git branch --show-current
echo ""

echo "🔄 Création d'un commit vide pour déclencher le workflow..."
git commit --allow-empty -m "chore: test deployment with Vercel secrets configured"

echo ""
echo "⬆️  Push vers GitHub..."
git push origin staging

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Push Réussi!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📍 Prochaines étapes:"
echo ""
echo "1. Aller sur GitHub Actions:"
echo "   https://github.com/Feyem9/E-COMMERCE_APP/actions"
echo ""
echo "2. Vérifier que le workflow 'Deploy to Staging' démarre"
echo ""
echo "3. Attendre ~5-10 minutes pour le déploiement complet"
echo ""
echo "4. Une fois terminé, le workflow devrait afficher ✅ Success!"
echo ""
echo "5. L'URL de staging sera visible dans les logs du workflow"
echo ""
echo "════════════════════════════════════════════════════════════════"

#!/bin/bash

# ========================================
# Script de Test Sentry
# Date: 19 Décembre 2025
# ========================================

echo "════════════════════════════════════════════════════════════════"
echo "  🧪 TEST SENTRY - Monitoring Production"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📝 Instructions:"
echo ""
echo "1. Ouvrir l'application en staging ou production"
echo "   - Staging: https://staging-market.vercel.app"
echo "   - Production: https://market-jet.vercel.app"
echo ""
echo "2. Ouvrir la console du navigateur (F12)"
echo ""
echo "3. Copier-coller ce code dans la console:"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
cat << 'EOF'
// Test 1: Erreur simple
try {
  throw new Error('🧪 Test Sentry - Erreur de test production');
} catch (error) {
  Sentry.captureException(error);
  console.log('✅ Erreur envoyée à Sentry');
}

// Test 2: Message personnalisé
Sentry.captureMessage('🧪 Test Sentry - Message de test', 'info');
console.log('✅ Message envoyé à Sentry');

// Test 3: Event avec contexte
Sentry.captureException(new Error('🧪 Test avec contexte'), {
  tags: { test: 'monitoring' },
  extra: { timestamp: new Date().toISOString() }
});
console.log('✅ Event avec contexte envoyé');

console.log('');
console.log('🎯 Maintenant, vérifiez sur Sentry:');
console.log('   1. Aller sur https://sentry.io/');
console.log('   2. Sélectionner le projet');
console.log('   3. Vérifier que les 3 erreurs/messages apparaissent');
EOF
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "4. Vérifier sur Sentry Dashboard:"
echo "   https://sentry.io/"
echo ""
echo "5. Vous devriez voir 3 nouveaux events:"
echo "   - Erreur de test"
echo "   - Message de test"
echo "   - Event avec contexte"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ Si les 3 events apparaissent → Sentry fonctionne parfaitement!"
echo "❌ Si rien n'apparaît → Vérifier la configuration DSN"
echo ""

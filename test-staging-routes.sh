#!/bin/bash

# Script de test complet des routes staging
# Date: 19 Décembre 2025

STAGING_URL="https://staging-market.vercel.app"

echo "════════════════════════════════════════════════════════════════"
echo "  🧪 Test Complet Routes Staging Frontend"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🔗 URL de staging: $STAGING_URL"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Fonction pour tester une route
test_route() {
    local route=$1
    local description=$2
    local url="${STAGING_URL}${route}"
    
    echo "📍 $description"
    echo "   Route: $route"
    
    # Test avec timeout de 10s
    response=$(curl -s -o /dev/null -w "%{http_code}|%{time_total}" --max-time 10 "$url" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        status_code=$(echo $response | cut -d'|' -f1)
        time_total=$(echo $response | cut -d'|' -f2)
        
        if [ "$status_code" = "200" ]; then
            echo "   ✅ Status: $status_code | Temps: ${time_total}s"
        elif [ "$status_code" = "401" ] || [ "$status_code" = "403" ]; then
            echo "   ⚠️  Status: $status_code (Protected) | Temps: ${time_total}s"
        elif [ "$status_code" = "404" ]; then
            echo "   ❌ Status: $status_code (Not Found) | Temps: ${time_total}s"
        else
            echo "   ⚠️  Status: $status_code | Temps: ${time_total}s"
        fi
    else
        echo "   ❌ Timeout ou erreur de connexion"
    fi
    
    echo ""
}

# Tests des routes principales
echo "🏠 PAGES PUBLIQUES"
echo "──────────────────────────────────────────────────────────────"
test_route "/" "Page d'accueil"
test_route "/home" "Home (alternative)"
test_route "/products" "Liste des produits"
test_route "/categories" "Catégories"
test_route "/help" "Page d'aide"

echo ""
echo "🔐 AUTHENTIFICATION"
echo "──────────────────────────────────────────────────────────────"
test_route "/login" "Page de connexion"
test_route "/register" "Page d'inscription"

echo ""
echo "👤 PAGES UTILISATEUR (Protected)"
echo "──────────────────────────────────────────────────────────────"
test_route "/profile" "Profil utilisateur"
test_route "/cart" "Panier"
test_route "/favorite" "Favoris"
test_route "/ordered" "Commandes"
test_route "/payment" "Payment"
test_route "/payment-success" "Payment Success"
test_route "/transaction" "Transactions"
test_route "/transaction-history" "Historique transactions"

echo ""
echo "🛠️  PAGES SPÉCIALES"
echo "──────────────────────────────────────────────────────────────"
test_route "/order-tracking" "Suivi de commande"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  📊 Résumé du Test"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🔗 URL testée: $STAGING_URL"
echo ""
echo "✅ = Route accessible (200)"
echo "⚠️  = Route protégée ou statut non-200"
echo "❌ = Route non trouvée ou erreur"
echo ""
echo "════════════════════════════════════════════════════════════════"

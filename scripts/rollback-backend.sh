#!/bin/bash

# ========================================
# Script de Rollback Backend (Render)
# Date: 19 Décembre 2025
# ========================================

echo "════════════════════════════════════════════════════════════════"
echo "  🔄 ROLLBACK BACKEND (Render)"
echo "════════════════════════════════════════════════════════════════"
echo ""

BACKEND_DIR="/home/christian/Bureau/CHRISTIAN/FullStackApp/backend/E-COMMERCE_APP"

# Vérifier que le dossier existe
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Dossier backend introuvable: $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR" || exit 1

echo "📋 Derniers commits:"
echo ""
git log --oneline --decorate -10

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Options de rollback:"
echo "  1. Revert d'un commit spécifique (recommandé)"
echo "  2. Reset hard à un commit (⚠️ destructif)"
echo "  3. Déploiement manual via Render Dashboard"
echo ""
read -p "Choisir option (1-3): " OPTION

case $OPTION in
    1)
        echo ""
        read -p "Entrer le hash du commit à revert: " COMMIT_HASH
        
        if [ -z "$COMMIT_HASH" ]; then
            echo "❌ Aucun hash fourni. Annulation."
            exit 1
        fi
        
        echo ""
        echo "🔄 Revert du commit $COMMIT_HASH..."
        git revert "$COMMIT_HASH" --no-edit
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Revert créé localement"
            echo ""
            read -p "Push vers GitHub et déclencher redéploiement? (y/n): " CONFIRM
            
            if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
                git push origin master
                echo ""
                echo "════════════════════════════════════════════════════════════════"
                echo "  ✅ ROLLBACK EN COURS"
                echo "════════════════════════════════════════════════════════════════"
                echo ""
                echo "⏱️  Render va redéployer automatiquement (2-5 minutes)"
                echo "🌐 Suivre sur: https://dashboard.render.com/"
                echo ""
            fi
        else
            echo "❌ Erreur lors du revert"
            exit 1
        fi
        ;;
        
    2)
        echo ""
        echo "⚠️  ATTENTION: Cette action est DESTRUCTIVE !"
        read -p "Entrer le hash du commit cible: " COMMIT_HASH
        
        if [ -z "$COMMIT_HASH" ]; then
            echo "❌ Aucun hash fourni. Annulation."
            exit 1
        fi
        
        echo ""
        read -p "Êtes-vous CERTAIN? (taper 'CONFIRMER' en majuscules): " CONFIRM
        
        if [ "$CONFIRM" = "CONFIRMER" ]; then
            git reset --hard "$COMMIT_HASH"
            git push -f origin master
            
            echo ""
            echo "════════════════════════════════════════════════════════════════"
            echo "  ✅ RESET EFFECTUÉ"
            echo "════════════════════════════════════════════════════════════════"
            echo ""
            echo "⏱️  Render va redéployer (2-5 minutes)"
            echo ""
        else
            echo "❌ Annulation du reset"
        fi
        ;;
        
    3)
        echo ""
        echo "📝 Rollback manuel via Render Dashboard:"
        echo ""
        echo "1. Aller sur: https://dashboard.render.com/"
        echo "2. Sélectionner le service backend"
        echo "3. Onglet 'Manual Deploy'"
        echo "4. Option 'Deploy a specific commit'"
        echo "5. Choisir le commit stable"
        echo "6. Cliquer 'Deploy'"
        echo ""
        ;;
        
    *)
        echo "❌ Option invalide"
        exit 1
        ;;
esac

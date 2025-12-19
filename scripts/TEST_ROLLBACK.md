# 🔄 Guide de Test Rollback

**Date**: 19 Décembre 2025  
**Objectif**: Tester que les scripts de rollback fonctionnent

---

## 🎯 TEST 1: Rollback Frontend (Vercel)

### **Préparation** (5 min)

Créons un changement mineur pour tester :

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Créer un fichier de test
echo "// Test de rollback - $(date)" >> src/app/app.component.ts

# Commit
git add src/app/app.component.ts
git commit -m "test: rollback test - à revert"

# Push vers staging
git push origin staging
```

**Attendre** : 5-10 minutes (déploiement Vercel)

### **Test de Rollback** (5 min)

```bash
# Lancer le script
./scripts/rollback-frontend.sh
```

**Actions** :
1. Le script liste les déploiements
2. Choisir le deployment AVANT le test
3. Confirmer le rollback
4. Vérifier sur https://staging-market.vercel.app

**Résultat attendu** :
- ✅ Version précédente restaurée
- ✅ Changement de test disparu
- ✅ Temps < 2 minutes

### **Nettoyage**

```bash
# Supprimer le commit de test
git revert HEAD --no-edit
git push origin staging
```

---

## 🎯 TEST 2: Rollback Backend (Render)

### **NOT** ⚠️ **Ce test est OPTIONNEL**

Le backend sur Render Free Tier prend 2-5 minutes à redémarrer.

**Si vous voulez tester** :

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/backend/E-COMMERCE_APP

# Créer changement mineur
echo "# Test rollback - $(date)" >> README.md

# Commit et push
git add README.md
git commit -m "test: rollback test backend"
git push origin master
```

**Attendre** : 2-5 minutes (déploiement Render)

**Rollback** :
```bash
cd ../../frontend/E-COMMERCE_APP
./scripts/rollback-backend.sh
```

**Résultat attendu** :
- ✅ Revert effectué
- ✅ Push automatique
- ✅ Render redéploie

---

## ✅ CHECKLIST

### **Frontend Rollback**
- [ ] Script testé
- [ ] Rollback réussi
- [ ] Temps mesuré: _____ minutes
- [ ] Cleanup effectué

### **Backend Rollback** (Optionnel)
- [ ] Script testé
- [ ] Rollback réussi
- [ ] Temps mesuré: _____ minutes
- [ ] Cleanup effectué

---

## 💡 **ALTERNATIVE RAPIDE**

Si vous n'avez PAS le temps de tester maintenant :

**Dry-run** (lecture seule) :

```bash
# Frontend
./scripts/rollback-frontend.sh
# Quitter sans choisir deployment (Ctrl+C)

# Backend
./scripts/rollback-backend.sh
# Choisir option 3 (juste lire les instructions)
```

**Considéré comme OK si** :
- ✅ Scripts s'exécutent sans erreur
- ✅ Commandes affichées semblent correctes
- ✅ Pas d'erreur de syntaxe

---

**Temps estimé** :
- Test complet: 30 min
- Dry-run: 5 min

**Recommandation** : Dry-run maintenant, test complet plus tard

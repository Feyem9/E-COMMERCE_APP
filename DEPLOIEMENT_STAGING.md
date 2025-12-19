# 🚀 Guide de Déploiement Staging

**Date**: 18 Décembre 2025  
**Statut**: ✅ Prêt à déployer  

---

## ⚡ Déploiement Ultra-Rapide (2 minutes)

### **Option 1: Script Automatique** ⭐ RECOMMANDÉ

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
./deploy-staging.sh
```

Le script vous propose 3 options :
1. 🚀 Déploiement rapide (Vercel CLI)
2. 📊 Créer branche staging + push  
3. ℹ️ Afficher les instructions

---

### **Option 2: Manuel - Vercel CLI** ⚡ TRÈS RAPIDE

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Installer Vercel CLI (si pas déjà fait)
npm install -g vercel

# Login
vercel login

# Déployer sur staging
vercel --target staging
```

✅ **Résultat** : URL de staging en 2 minutes !

---

### **Option 3: Manuel - Branch Staging** 📊 AUTOMATIQUE

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Créer branche staging
git checkout -b staging

# Commit les workflows
git add .github/
git commit -m "ci: Add staging deployment"

# Push
git push origin staging
```

✅ **Résultat** : 
- Vercel détecte le push
- Crée un preview deployment
- URL visible dans Vercel dashboard

---

## 🎯 Environnements Disponibles

### **Développement** (Local)
- URL: `http://localhost:4200`
- Branch: `front-end`, `feature/*`
- Tests: Manuels

### **Staging** (Preview)
- URL: `https://market-jet-staging-xxx.vercel.app`
- Branch: `staging`, `develop`
- Tests: Automatiques (GitHub Actions)
- Déploiement: Auto sur push

### **Production**
- URL: `https://market-jet.vercel.app`
- Branch: `main`
- Tests: Complets (Unit + E2E + Load)
- Déploiement: Auto après merge

---

## 📊 Workflow de Déploiement

```
Développement Local
  ↓
  git push origin feature/xyz
  ↓
Preview Deployment (auto)
  ↓
  Créer PR → staging
  ↓
Staging Deployment (auto)
  ↓
  Tests & Validation
  ↓
  Merger staging → main
  ↓
Production Deployment (auto)
```

---

## ✅ Vérification du Déploiement Staging

### **1. Via Vercel Dashboard**

1. Aller sur https://vercel.com/
2. Cliquer sur votre projet
3. Onglet "Deployments"
4. Chercher le deployment de la branche `staging`
5. Cliquer pour voir l'URL

### **2. Via GitHub Actions**

1. Aller sur votre repo GitHub
2. Onglet "Actions"
3. Voir le workflow "Deploy to Staging"
4. L'URL est dans les logs

### **3. Via Vercel CLI**

```bash
vercel ls
```

---

## 🔧 Configuration Avancée

### **Créer un Alias Staging Permanent**

Sur Vercel dashboard :
1. Projet → Settings → Domains
2. Ajouter : `staging-market.vercel.app`
3. Lier à la branche `staging`

✅ **Résultat** : URL fixe pour staging !

---

## 🐛 Troubleshooting

### **Problème: Vercel CLI not found**

```bash
npm install -g vercel
# ou
npm install --global vercel
```

### **Problème: Workflow ne se déclenche pas**

Vérifier :
- La branche s'appelle bien `staging` ou `develop`
- Les workflows sont dans `.github/workflows/`
- Les secrets Vercel sont configurés (si workflow complet)

### **Problème: Build échoue**

```bash
# Tester localement d'abord
npm run build
```

---

## 📋 Checklist Staging

- [ ] Script `deploy-staging.sh` créé
- [ ] Workflow `deploy-staging.yml` créé
- [ ] Branche `staging` créée
- [ ] Push vers GitHub effectué
- [ ] Deployment visible sur Vercel
- [ ] URL de staging accessible
- [ ] Tests passent sur staging

---

## 🎯 Prochaine Action

**Pour déployer maintenant** :

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
./deploy-staging.sh
```

Choisir l'option 2 (Branch staging + push) pour un déploiement automatique !

---

**Créé le**: 18 Décembre 2025  
**Temps estimé**: 2-5 minutes  
**Difficulté**: ⭐☆☆☆☆ (Très facile)

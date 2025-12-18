# 🔄 CI/CD avec GitHub Actions - Guide Complet

**Date**: 18 Décembre 2025  
**Statut**: ✅ Configuré  
**Workflows**: 2 fichiers créés

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Fichiers créés](#fichiers-créés)
3. [Configuration requise](#configuration-requise)
4. [Étapes d'activation](#étapes-dactivation)
5. [Workflows disponibles](#workflows-disponibles)
6. [Secrets à configurer](#secrets-à-configurer)
7. [Utilisation](#utilisation)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Vue d'ensemble

Deux workflows GitHub Actions ont été créés :

### 1️⃣ **CI Simple** (`ci-simple.yml`)
Configuration minimaliste pour démarrer rapidement :
- ✅ Tests unitaires
- ✅ Build de production
- ⏱️ Durée: ~5-10 minutes

### 2️⃣ **CI/CD Complet** (`ci.yml`)
Configuration professionnelle complète :
- ✅ Linting
- ✅ Tests unitaires
- ✅ Tests E2E (Cypress)
- ✅ Build de production
- ✅ Tests de charge (K6) - optionnel
- ✅ Déploiement automatique Vercel
- ✅ Preview deployments
- ⏱️ Durée: ~15-20 minutes

---

## 📂 Fichiers Créés

```
.github/
└── workflows/
    ├── ci-simple.yml      ← Configuration simple (recommandé pour démarrer)
    └── ci.yml             ← Configuration complète (production)
```

---

## ⚙️ Configuration Requise

### **Prérequis GitHub**

1. **Repository GitHub** avec le code
2. **Branch `main`** (ou `front-end` selon votre config)
3. **Secrets GitHub** configurés (voir section ci-dessous)

---

## 🔐 Secrets à Configurer

Pour activer le déploiement automatique vers Vercel, vous devez ajouter 3 secrets dans GitHub :

### **Étapes pour ajouter les secrets**:

1. **Aller sur GitHub** :
   ```
   https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions
   ```

2. **Cliquer sur "New repository secret"**

3. **Ajouter ces 3 secrets** :

#### 1️⃣ **VERCEL_TOKEN**

**Comment l'obtenir**:
```bash
# 1. Installer Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Générer un token
# Aller sur: https://vercel.com/account/tokens
# Créer un nouveau token
```

**Valeur**: Le token généré (commence par `"vercel_...")

---

#### 2️⃣ **VERCEL_ORG_ID**

**Comment l'obtenir**:
```bash
# Dans votre projet local
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Lier le projet Vercel (si pas déjà fait)
vercel link

# Le fichier .vercel/project.json contiendra l'orgId
cat .vercel/project.json
```

**Ou sur le dashboard Vercel**:
1. Aller sur https://vercel.com/
2. Settings → General
3. Copier "Team ID" ou "Organization ID"

---

#### 3️⃣ **VERCEL_PROJECT_ID**

**Comment l'obtenir**:
```bash
# Dans le même fichier .vercel/project.json
cat .vercel/project.json | grep projectId
```

**Ou sur le dashboard Vercel**:
1. Aller sur votre projet
2. Settings → General
3. Copier "Project ID"

---

## 🚀 Étapes d'Activation

### **Option A: Démarrage Rapide (CI Simple)**

1. **Commit et push** les workflows :
   ```bash
   cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
   
   git add .github/
   git commit -m "ci: Add GitHub Actions CI workflow"
   git push origin front-end
   ```

2. **Vérifier sur GitHub**:
   - Aller dans l'onglet "Actions"
   - Le workflow devrait démarrer automatiquement

3. **C'est tout !** ✅

---

### **Option B: Configuration Complète (CI/CD)**

1. **Ajouter les secrets** (voir section ci-dessus)

2. **Désactiver ci-simple.yml** (optionnel) :
   ```bash
   # Renommer pour désactiver
   mv .github/workflows/ci-simple.yml .github/workflows/ci-simple.yml.disabled
   ```

3. **Commit et push** :
   ```bash
   git add .github/
   git commit -m "ci: Add complete CI/CD pipeline with Vercel deployment"
   git push origin front-end
   ```

4. **Merger vers main** pour activer le déploiement production

---

## 📊 Workflows Disponibles

### **1. CI Simple** (ci-simple.yml)

**Déclenché sur**:
- Push vers `main` ou `front-end`
- Pull Request vers `main`

**Jobs**:
```
🧪 Test & Build
  ├─ 📥 Checkout code
  ├─ 📦 Setup Node.js 18
  ├─ 📥 Install dependencies
  ├─ 🧪 Run unit tests
  ├─ 🏗️ Build
  └─ ✅ Success
```

**Durée moyenne**: 5-10 minutes

---

### **2. CI/CD Complet** (ci.yml)

**Déclenché sur**:
- Push vers `main`, `front-end`, `develop`
- Pull Request vers `main` ou `front-end`

**Jobs**:

```
┌──────────────────────────────────────┐
│ 1️⃣ Lint Code                        │
│    ├─ ESLint (si configuré)         │
│    └─ Code quality checks           │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 2️⃣ Unit Tests                       │
│    ├─ Karma + Jasmine               │
│    ├─ Code coverage                 │
│    └─ Upload coverage report        │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 3️⃣ E2E Tests (Cypress)              │
│    ├─ Build app                     │
│    ├─ Start dev server              │
│    ├─ Run Cypress tests             │
│    └─ Upload screenshots/videos     │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 4️⃣ Build Application                │
│    ├─ Production build              │
│    ├─ Analyze bundle size           │
│    └─ Upload artifacts              │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 5️⃣ Load Tests (K6) - Optional       │
│    └─ Test production URL           │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 6️⃣ Deploy (Production)              │
│    ├─ Only on main branch           │
│    ├─ Deploy to Vercel              │
│    └─ Update production URL         │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 7️⃣ Deploy (Preview)                 │
│    ├─ On Pull Requests              │
│    ├─ Deploy preview                │
│    └─ Comment PR with URL           │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│ 8️⃣ Notifications                    │
│    └─ Send success/failure alerts   │
└──────────────────────────────────────┘
```

**Durée moyenne**: 15-20 minutes

---

## 🎯 Utilisation

### **Scénario 1: Push sur branche de développement**

```bash
git add .
git commit -m "feat: Add new feature"
git push origin front-end
```

**Résultat**:
- ✅ Tests unitaires exécutés
- ✅ Tests E2E exécutés
- ✅ Build créé
- 🔍 Preview deployment créé (si configuré)

---

### **Scénario 2: Merge vers main (Production)**

```bash
git checkout main
git merge front-end
git push origin main
```

**Résultat**:
- ✅ Tous les tests exécutés
- ✅ Build créé
- ✅ Tests de charge K6 (optionnel)
- 🚀 **Déploiement automatique vers production**
- 📧 Notifications envoyées

---

### **Scénario 3: Pull Request**

```bash
# Créer une PR sur GitHub
# front-end → main
```

**Résultat**:
- ✅ Tous les tests exécutés
- ✅ Build créé
- 🔍 Preview deployment créé
- 💬 Commentaire automatique avec l'URL de preview

---

## 🐛 Troubleshooting

### **Problème 1: Workflow ne se déclenche pas**

**Solutions**:
1. Vérifier que les fichiers sont dans `.github/workflows/`
2. Vérifier l'extension `.yml` (pas `.yaml`)
3. Vérifier la syntaxe YAML (indentation)
4. Push vers une branche surveillée (`main`, `front-end`)

---

### **Problème 2: Tests échouent sur GitHub mais passent localement**

**Causes possibles**:
- Variables d'environnement manquantes
- Différences Node.js version
- Dépendances manquantes

**Solutions**:
```yaml
# Dans le workflow, ajouter:
env:
  CI: true
  NODE_OPTIONS: --max_old_space_size=4096
```

---

### **Problème 3: Déploiement Vercel échoue**

**Vérifications**:
1. Secrets correctement configurés?
   ```
   VERCEL_TOKEN
   VERCEL_ORG_ID
   VERCEL_PROJECT_ID
   ```

2. Token Vercel valide?
   - Régénérer si nécessaire sur https://vercel.com/account/tokens

3. Permissions correctes?
   - Le token doit avoir accès au projet

---

### **Problème 4: Tests E2E timeout**

**Solutions**:
```yaml
# Augmenter le timeout dans le workflow
- name: Run Cypress E2E tests
  uses: cypress-io/github-action@v6
  with:
    wait-on-timeout: 180  # 3 minutes au lieu de 120
```

---

### **Problème 5: Build manque de mémoire**

**Solutions**:
```yaml
- name: Build
  run: npm run build
  env:
    NODE_OPTIONS: --max_old_space_size=8192  # 8GB
```

---

## 📊 Badges GitHub Actions

Ajouter des badges dans votre `README.md` :

```markdown
![CI/CD](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%2FCD%20Pipeline%20-%20E-Commerce%20App/badge.svg)
![Tests](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/YOUR_REPO/ci.yml?label=tests)
```

---

## 🎯 Optimisations Possibles

### **1. Cache des dépendances**

✅ **Déjà configuré** avec `cache: 'npm'`

### **2. Matrix strategy (tester plusieurs versions)**

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [18, 20]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
```

### **3. Parallel jobs**

✅ **Déjà configuré** : unit tests et E2E tests en parallèle

### **4. Conditional jobs**

✅ **Déjà configuré** : déploiement uniquement sur `main`

---

## 📝 Checklist de Configuration

- [ ] Fichiers workflows créés dans `.github/workflows/`
- [ ] Secrets Vercel ajoutés sur GitHub
- [ ] Tests unitaires passent localement
- [ ] Tests E2E passent localement
- [ ] Build fonctionne localement
- [ ] Push vers GitHub
- [ ] Workflow se déclenche automatiquement
- [ ] Tests passent sur GitHub Actions
- [ ] Déploiement automatique fonctionne (si configuré)
- [ ] Badges ajoutés au README

---

## 🎓 Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vercel GitHub Integration](https://vercel.com/docs/git/vercel-for-github)
- [Cypress GitHub Actions](https://github.com/cypress-io/github-action)
- [Node.js GitHub Actions](https://github.com/actions/setup-node)

---

## 🎉 Conclusion

Vous avez maintenant un pipeline CI/CD complet et professionnel ! 🚀

**Avantages**:
- ✅ Tests automatiques à chaque commit
- ✅ Build validé avant merge
- ✅ Déploiement automatique en production
- ✅ Preview deployments pour les PRs
- ✅ Notifications en cas de problème

**Prochaine action**:
```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
git add .github/
git commit -m "ci: Add GitHub Actions CI/CD pipeline"
git push
```

---

**Créé le**: 18 Décembre 2025  
**Version**: 1.0.0  
**Statut**: ✅ Prêt à l'emploi

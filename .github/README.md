# 🔄 GitHub Actions CI/CD

Pipeline d'intégration et déploiement continus pour l'application E-Commerce.

---

## 📂 Contenu

- **📊 Workflows** (2):
  - `ci-simple.yml` - Configuration simple ⭐
  - `ci.yml` - Configuration complète avec déploiement

- **📚 Documentation** (4):
  - `README.md` - Ce fichier
  - `DEMARRAGE_RAPIDE.md` - Guide de 10 minutes
  - `GITHUB_ACTIONS_GUIDE.md` - Guide technique complet
  - `CI_CD_MISSION_ACCOMPLIE.md` - Récapitulatif

- **⚙️ Utilitaires** (1):
  - `get-vercel-secrets.sh` - Helper pour secrets Vercel

---

## 🚀 Démarrage Ultra-Rapide

```bash
# 1. Commit les fichiers
git add .github/
git commit -m "ci: Add GitHub Actions CI/CD"
git push

# 2. Vérifier sur GitHub
# Onglet "Actions" → workflow se déclenche automatiquement
```

**C'est tout ! Les tests s'exécutent automatiquement.** ✅

---

## 📖 Documentation

| Fichier | But | Durée |
|---------|-----|-------|
| `DEMARRAGE_RAPIDE.md` | Configuration rapide | 10 min |
| `GITHUB_ACTIONS_GUIDE.md` | Guide technique détaillé | - |
| `CI_CD_MISSION_ACCOMPLIE.md` | Vue d'ensemble complète | - |

---

## ⚡ Workflows Disponibles

### **CI Simple** (`ci-simple.yml`)

- Tests unitaires
- Build de production
- Durée: ~5-10 min
- **Status**: ✅ Prêt à l'emploi

### **CI/CD Complet** (`ci.yml`)

- Linting + Tests + E2E + Build
- Déploiement automatique Vercel
- Tests de charge K6
- Durée: ~15-20 min
- **Status**: ⚠️ Nécessite secrets Vercel

---

## 🔐 Configuration Secrets

Pour le déploiement automatique:

```bash
# Récupérer les secrets
./get-vercel-secrets.sh

# Ajouter sur GitHub:
# Settings → Secrets and variables → Actions
# - VERCEL_TOKEN
# - VERCEL_ORG_ID  
# - VERCEL_PROJECT_ID
```

---

## 📊 Statut Actuel

- ✅ Workflows configurés
- ✅ Documentation complète
- ✅ Helper scripts créés
- ⏳ En attente: Push vers GitHub

---

**Créé le**: 18 Décembre 2025  
**Version**: 1.0.0  
**Statut**: ✅ Prêt à utiliser

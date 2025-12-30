# 🔧 Problèmes Résolus - Déploiement Staging

**Date**: 19 Décembre 2025  
**Session**: Déploiement Staging avec GitHub Actions

---

## 📋 Problèmes Rencontrés et Solutions

### **Problème 1: Secrets Manquants** ❌ → ✅

**Erreur** :
```
Error: Input required and not supplied: vercel-token
```

**Cause** :
- Les secrets Vercel n'étaient pas configurés sur GitHub

**Solution** :
1. Obtenu les 3 secrets Vercel :
   - VERCEL_TOKEN
   - VERCEL_ORG_ID
   - VERCEL_PROJECT_ID

2. Ajoutés sur GitHub :
   - https://github.com/Feyem9/E-COMMERCE_APP/settings/secrets/actions

**Résultat** : ✅ Secrets configurés

---

### **Problème 2: Output Directory Incorrect** ❌ → ✅

**Erreur** :
```
No Output Directory named "market" found after the Build completed.
```

**Cause** :
- Vercel cherchait `market/` mais Angular build génère `dist/market/browser/`
- Pas de `vercel.json` configuré

**Solution** :
1. Créé `vercel.json` avec :
   ```json
   {
     "outputDirectory": "dist/market/browser"
   }
   ```

2. Commit et push

**Résultat** : ✅ Output directory correct

---

### **Problème 3: Configuration Vercel Incompatible** ❌ → ✅

**Erreur** :
```
Error! If `rewrites`, `redirects`, `headers`, `cleanUrls` or `trailingSlash` 
are used, then `routes` cannot be present.
```

**Cause** :
- Utilisation de `routes` (ancien) + `headers` (nouveau) ensemble
- Incompatible dans Vercel v2+

**Solution** :
1. Remplacé `routes` par `rewrites` :
   ```json
   // Avant
   "routes": [{ "src": "/(.*)", "dest": "/index.html" }]
   
   // Après
   "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
   ```

2. Gardé `headers` (compatible avec `rewrites`)

**Résultat** : ✅ Configuration compatible Vercel v2

---

## ✅ Configuration Finale `vercel.json`

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "dist/market/browser",
  "framework": "angular",
  "installCommand": "npm install --legacy-peer-deps",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

---

## 🎯 Résumé des Commits

1. **64894d5** : "fix: add vercel.json with correct output directory"
   - Ajout du fichier vercel.json
   - Configuration output directory

2. **be0a80b** : "fix: use rewrites instead of routes in vercel.json for v2 compatibility"
   - Migration routes → rewrites
   - Compatibilité Vercel v2

---

## 📊 État Final

| Configuration | Avant | Après |
|---------------|-------|-------|
| **Secrets Vercel** | ❌ 0/3 | ✅ 3/3 |
| **vercel.json** | ❌ Absent | ✅ Présent |
| **Output Directory** | ❌ Incorrect | ✅ `dist/market/browser` |
| **Routing Config** | ❌ `routes` (incompatible) | ✅ `rewrites` (compatible) |
| **Headers** | ❌ Conflictuel | ✅ Compatible |
| **Workflow** | ❌ Failed | ⏳ En cours... |

---

## 🚀 Prochaine Étape

**Workflow en cours** :
- URL: https://github.com/Feyem9/E-COMMERCE_APP/actions

**Résultat attendu** :
- ✅ Deploy to Vercel : Success
- ✅ URL de staging disponible
- ✅ Application accessible

**Temps estimé** : ~5-7 minutes

---

## 💡 Leçons Apprises

### **1. Secrets Vercel**
- Toujours configurer les 3 secrets avant de déployer
- TOKEN, ORG_ID, PROJECT_ID

### **2. Angular + Vercel**
- Le build Angular 18 génère `dist/[project-name]/browser/`
- Toujours spécifier dans `vercel.json`

### **3. Vercel v2 Configuration**
- Utiliser `rewrites` au lieu de `routes`
- `rewrites` compatible avec `headers`, `redirects`, etc.
- `routes` incompatible avec propriétés modernes

### **4. Debugging**
- Lire attentivement les messages d'erreur Vercel
- Consulter la doc : https://vercel.com/docs

---

## ✅ Checklist Finale

- [x] Secrets Vercel configurés
- [x] vercel.json créé
- [x] Output directory correct
- [x] Rewrites au lieu de routes
- [x] Headers configurés
- [x] Commits pushés
- [ ] Workflow réussi ← En cours...
- [ ] URL de staging accessible
- [ ] Application testée

---

**Créé le**: 19 Décembre 2025, 11:52 AM  
**Statut**: ⏳ En attente du workflow  
**Prochaine action**: Vérifier le résultat sur GitHub Actions

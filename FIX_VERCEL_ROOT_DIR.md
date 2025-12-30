# 🔧 Fix Vercel Root Directory Error

**Error**: "The specified Root Directory 'src' does not exist"

---

## 🎯 SOLUTION

### **Via Vercel Dashboard** :

1. **Aller sur** : https://vercel.com/

2. **Projet** : market (ou staging-market)

3. **Settings** :
   - Cliquer sur "Settings"
   - Onglet "General"

4. **Root Directory** :
   - Trouver section "Root Directory"
   - **Changer** : `src` → **VIDE** (laisser vide)
   - OU mettre : `.`

5. **Build Settings** :
   - Framework Preset: **Angular**
   - Build Command: `npm run build -- --configuration production`
   - Output Directory: `dist/market/browser`
   - Install Command: `npm install --legacy-peer-deps`

6. **Save**

7. **Redeploy** :
   - Onglet "Deployments"
   - Dernier deployment → "..." → "Redeploy"

---

## 📊 Configuration Correcte

```json
{
  "Root Directory": "",  // OU "."
  "Framework": "Angular",
  "Build Command": "npm run build -- --configuration production",
  "Output Directory": "dist/market/browser",
  "Install Command": "npm install --legacy-peer-deps"
}
```

---

## 📁 Structure Attendue

```
frontend/E-COMMERCE_APP/
├── src/              ← Le code source Angular
├── dist/             ← Output du build
├── node_modules/
├── package.json
├── angular.json
├── vercel.json
└── ...
```

**Vercel doit démarrer à la racine** : `frontend/E-COMMERCE_APP/`  
**PAS** dans un sous-dossier `src/`

---

## ✅ Vérification

Après modification, vérifier :

1. **Settings** → Root Directory = vide ou `.`
2. **Redeploy**
3. Vérifier logs : aucune erreur "src does not exist"
4. ✅ Build réussi !

---

**Créé le** : 19 Décembre 2025  
**Fix pour** : Erreur Root Directory Vercel

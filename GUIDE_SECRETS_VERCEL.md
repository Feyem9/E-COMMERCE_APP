# 🔐 Guide: Configuration des Secrets Vercel pour GitHub Actions

**Date**: 19 Décembre 2025  
**Objectif**: Configurer 3 secrets pour activer le déploiement automatique

---

## 📋 Les 3 Secrets Nécessaires

| Secret | Description | Où le trouver |
|--------|-------------|---------------|
| **VERCEL_TOKEN** | Token d'authentification | https://vercel.com/account/tokens |
| **VERCEL_ORG_ID** | ID de l'organisation | Settings → Team ID |
| **VERCEL_PROJECT_ID** | ID du projet | Project Settings → Project ID |

---

## 🎯 ÉTAPE 1: Obtenir VERCEL_PROJECT_ID

1. Aller sur : **https://vercel.com/**

2. Cliquer sur votre projet : **e-commerce-app**

3. Cliquer sur **"Settings"** (onglet en haut)

4. Section **"General"**

5. Chercher **"Project ID"**
   ```
   Exemple: prj_abc123xyz456
   ```

6. **COPIER** cette valeur

✅ **SECRET 1 obtenu !**

---

## 🎯 ÉTAPE 2: Obtenir VERCEL_ORG_ID

### **Méthode A: Via Settings** ⭐ PLUS SIMPLE

1. Sur Vercel, cliquer sur votre **avatar/nom** (coin supérieur droit)

2. Cliquer sur **"Account Settings"** ou **"Team Settings"**

3. Chercher **"Team ID"** ou **"Organization ID"**
   ```
   Exemple: team_abc123xyz456
   ```

4. **COPIER** cette valeur

### **Méthode B: Via URL**

L'Organization ID est visible dans l'URL de votre projet :
```
https://vercel.com/[ORG_ID]/[PROJECT_NAME]
                    ^^^^^^^ c'est ça!
```

Par exemple dans : `https://vercel.com/christians-projects-9c9bef59/e-commerce-app`
- ORG_ID = `christians-projects-9c9bef59`

✅ **SECRET 2 obtenu !**

---

## 🎯 ÉTAPE 3: Créer VERCEL_TOKEN

1. Aller sur : **https://vercel.com/account/tokens**

2. Cliquer sur **"Create Token"** (bouton bleu)

3. **Remplir le formulaire** :
   ```
   Token Name: GitHub Actions CI/CD
   Scope: Full Account
   Expiration: No Expiration (ou 1 year)
   ```

4. Cliquer sur **"Create Token"**

5. **⚠️ IMPORTANT** : Le token s'affiche **UNE SEULE FOIS** !
   ```
   Format: vercel_xxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **COPIER IMMÉDIATEMENT** le token

✅ **SECRET 3 obtenu !**

---

## 🔧 ÉTAPE 4: Ajouter les Secrets sur GitHub

### **A. Aller sur la page des secrets**

URL: https://github.com/Feyem9/E-COMMERCE_APP/settings/secrets/actions

### **B. Ajouter le premier secret**

1. Cliquer sur **"New repository secret"** (bouton vert)

2. Remplir :
   ```
   Name: VERCEL_TOKEN
   Value: (coller le token copié à l'étape 3)
   ```

3. Cliquer **"Add secret"**

### **C. Ajouter le deuxième secret**

1. Cliquer encore sur **"New repository secret"**

2. Remplir :
   ```
   Name: VERCEL_ORG_ID
   Value: (coller l'Organization ID de l'étape 2)
   ```

3. Cliquer **"Add secret"**

### **D. Ajouter le troisième secret**

1. Cliquer encore sur **"New repository secret"**

2. Remplir :
   ```
   Name: VERCEL_PROJECT_ID
   Value: (coller le Project ID de l'étape 1)
   ```

3. Cliquer **"Add secret"**

---

## ✅ VÉRIFICATION

Vous devriez voir 3 secrets dans la liste :

```
✓ VERCEL_TOKEN          Updated X minutes ago
✓ VERCEL_ORG_ID         Updated X minutes ago
✓ VERCEL_PROJECT_ID     Updated X minutes ago
```

---

## 🚀 ÉTAPE 5: Tester le Workflow

Une fois les 3 secrets ajoutés :

1. **Retourner sur votre terminal**

2. **Faire un petit changement et push** :
   ```bash
   cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
   git checkout staging
   git commit --allow-empty -m "chore: test deployment with secrets"
   git push origin staging
   ```

3. **Vérifier sur GitHub** :
   - https://github.com/Feyem9/E-COMMERCE_APP/actions
   - Le workflow devrait réussir cette fois ! ✅

---

## 🐛 Troubleshooting

### **Problème: Token invalide**

- Régénérer un nouveau token sur Vercel
- Mettre à jour le secret `VERCEL_TOKEN` sur GitHub

### **Problème: Organization ID incorrect**

- Vérifier dans l'URL ou dans Account Settings
- Format attendu : `team_xxxxx` ou similaire

### **Problème: Project ID incorrect**

- Retourner dans Project Settings
- Copier exactement le Project ID affiché

---

## 📊 Résultat Attendu

Après configuration :

| Avant | Après |
|-------|-------|
| ❌ Deploy to Vercel: Failed | ✅ Deploy to Vercel: Success |
| ⚠️ Secrets manquants | ✅ 3 secrets configurés |
| ❌ Workflow échoue | ✅ Workflow réussit |

---

## 💡 Conseils

- **Sécurité** : Ne partagez JAMAIS vos tokens
- **Expiration** : Notez la date d'expiration du token
- **Backup** : Gardez les IDs dans un endroit sûr

---

## ✅ Checklist Finale

- [ ] VERCEL_PROJECT_ID obtenu
- [ ] VERCEL_ORG_ID obtenu
- [ ] VERCEL_TOKEN créé
- [ ] Les 3 secrets ajoutés sur GitHub
- [ ] Workflow testé et réussi

---

**Créé le**: 19 Décembre 2025  
**Temps estimé**: 10 minutes  
**Difficulté**: ⭐⭐☆☆☆ (Facile avec ce guide)

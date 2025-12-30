# 🧪 Guide de Test Manuel - Staging Frontend

**Date**: 19 Décembre 2025  
**URL Staging**: https://staging-market.vercel.app  
**Statut**: ✅ Déployé avec protection Vercel

---

## 🔐 Accès au Staging

### **Étape 1: Se Connecter à Vercel**

1. Ouvrir le navigateur
2. Aller sur : **https://staging-market.vercel.app**
3. Vous verrez une page d'authentification Vercel
4. Cliquer sur "Continue with Vercel"
5. Se connecter avec votre compte Vercel

**Résultat**: Vous serez redirigé vers l'application staging

---

## ✅ Checklist de Test

### **1. Pages Publiques** 🏠

- [ ] **Page d'accueil** (`/`)
  - Affichage des produits
  - Navigation fonctionne
  - Images chargent correctement
  - Pas d'erreurs dans la console

- [ ] **Liste des produits** (`/products`)
  - Tous les produits s'affichent
  - Recherche fonctionne
  - Filtres fonctionnent
  - Pagination fonctionne

- [ ] **Catégories** (`/categories`)
  - Liste des catégories visible
  - Clic sur catégorie fonctionne
  - Produits filtrés par catégorie

- [ ] **Page d'aide** (`/help`)
  - Contenu affiché
  - Liens fonctionnent

---

### **2. Authentification** 🔐

- [ ] **Page de connexion** (`/login`)
  - Formulaire s'affiche
  - Validation fonctionne
  - Messages d'erreur appropriés
  - Connexion réussie redirige

- [ ] **Page d'inscription** (`/register`)
  - Formulaire s'affiche
  - Tous les champs présents
  - Validation fonctionne
  - Inscription réussie

**Identifiants de test** (si configurés):
```
Email: test@example.com
Password: Test123!
```

---

### **3. Fonctionnalités Utilisateur** 👤

Après connexion, tester :

- [ ] **Profil** (`/profile`)
  - Informations utilisateur affichées
  - Modification possible
  - Sauvegarde fonctionne

- [ ] **Panier** (`/cart`)
  - Ajout produit au panier
  - Suppression produit du panier
  - Modification quantité
  - Total calculé correctement

- [ ] **Favoris** (`/favorite`)
  - Ajout aux favoris
  - Suppression des favoris
  - Liste correcte

- [ ] **Commandes** (`/ordered`)
  - Historique commandes visible
  - Détails commande accessibles
  - Statuts corrects

---

### **4. Processus d'Achat** 💳

- [ ] **Ajout au panier**
  - Depuis page produits
  - Depuis détail produit
  - Quantité modifiable

- [ ] **Page de paiement** (`/payment`)
  - Formulaire affiché
  - Validation champs
  - Total correct

- [ ] **Succès paiement** (`/payment-success`)
  - Message de confirmation
  - Détails commande
  - Redirection appropriée

---

### **5. Transactions** 💰

- [ ] **Transactions** (`/transaction`)
  - Liste des transactions
  - Détails visibles
  - Montants corrects

- [ ] **Historique** (`/transaction-history`)
  - Toutes les transactions
  - Filtre par date
  - Export possible (si implémenté)

---

### **6. Fonctionnalités Spéciales** 🛠️

- [ ] **Suivi de commande** (`/order-tracking`)
  - Formulaire recherche
  - Statut commande affiché
  - Timeline visible

---

## 🔍 Tests Techniques

### **Console du Navigateur**

1. Ouvrir DevTools (F12)
2. Onglet **Console**
3. Vérifier :
   - [ ] Pas d'erreurs JavaScript
   - [ ] Pas d'erreurs de chargement
   - [ ] Pas d'erreurs API

### **Network**

1. Onglet **Network**
2. Vérifier :
   - [ ] Requêtes API réussissent (200 OK)
   - [ ] Images chargent
   - [ ] Temps de réponse acceptable (< 2s)

### **Performance**

1. Onglet **Performance**
2. Vérifier :
   - [ ] First Contentful Paint < 2s
   - [ ] Time to Interactive < 3s
   - [ ] Pas de long tasks

---

## 📊 Rapport de Test

### **Template à remplir**:

```
Date du test: _______________
Navigateur: _________________
Version: ____________________

Pages testées: ___/16
Bugs trouvés: _______________
Bugs critiques: _____________

Fonctionnalités OK:
- [ ] Navigation
- [ ] Authentification
- [ ] Panier
- [ ] Paiement
- [ ] Profil

Bugs identifiés:
1. ________________________________
2. ________________________________
3. ________________________________

Performance:
- Vitesse: ⭐⭐⭐⭐⭐ (1-5)
- UX: ⭐⭐⭐⭐⭐ (1-5)
- Design: ⭐⭐⭐⭐⭐ (1-5)

Recommandations:
________________________________
________________________________
________________________________

Ready for production: ☐ OUI ☐ NON
```

---

## 🐛 Bugs Communs à Vérifier

### **Navigation**
- Liens morts
- Redirections incorrectes
- Routing cassé

### **Formulaires**
- Validation manquante
- Messages d'erreur peu clairs
- Soumission multiple possible

### **API**
- Endpoints non disponibles
- Timeouts
- Erreurs 500

### **UI/UX**
- Images manquantes
- CSS cassé
- Responsive non fonctionnel
- Textes coupés

---

## ✅ Validation Finale

Avant de passer en production, vérifier :

- [ ] **Tous les tests passent**
- [ ] **Aucun bug critique**
- [ ] **Performance acceptable**
- [ ] **Tous les formulaires fonctionnent**
- [ ] **Paiement test fonctionne**
- [ ] **Backend répond correctement**
- [ ] **Images et assets chargent**
- [ ] **Responsive fonctionne (mobile/tablet)**

---

## 🎯 URLs de Test Rapide

Copier-coller dans le navigateur (après authentification):

```
# Pages publiques
https://staging-market.vercel.app/
https://staging-market.vercel.app/products
https://staging-market.vercel.app/categories
https://staging-market.vercel.app/help

# Authentification
https://staging-market.vercel.app/login
https://staging-market.vercel.app/register

# Utilisateur (nécessite connexion)
https://staging-market.vercel.app/profile
https://staging-market.vercel.app/cart
https://staging-market.vercel.app/favorite
https://staging-market.vercel.app/ordered

# Paiement
https://staging-market.vercel.app/payment
https://staging-market.vercel.app/payment-success

# Transactions
https://staging-market.vercel.app/transaction
https://staging-market.vercel.app/transaction-history

# Spécial
https://staging-market.vercel.app/order-tracking
```

---

## 💡 Conseils

### **Navigation Rapide**
- Utiliser les DevTools (F12)
- Tester en mode Incognito
- Tester sur différents navigateurs

### **Documentation**
- Prendre des screenshots des bugs
- Noter les étapes de reproduction
- Vérifier la console pour les erreurs

### **Comparaison**
- Comparer avec production: https://market-jet.vercel.app
- Noter les différences
- Valider les nouvelles features

---

## 🚀 Après le Test

### **Si tout fonctionne** ✅
1. Documenter les résultats
2. Créer PR: `staging → main`
3. Merger après review
4. Déploiement auto en production

### **Si bugs trouvés** ❌
1. Créer issues sur GitHub
2. Corriger les bugs sur staging
3. Re-tester
4. Valider à nouveau

---

**Créé le**: 19 Décembre 2025  
**URL Staging**: https://staging-market.vercel.app  
**Status**: ✅ Ready to Test

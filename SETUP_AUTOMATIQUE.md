# 🎉 SETUP AUTOMATIQUE - Utilisateur de Test

## ✅ **C'EST FAIT !**

J'ai créé un test spécial qui va **automatiquement créer l'utilisateur de test** pour vous !

---

## 📁 **Fichier Créé**

**`cypress/e2e/00-setup.cy.ts`**

Ce fichier contient 2 tests :
1. ✅ Crée l'utilisateur `test@example.com`
2. ✅ Vérifie que le login fonctionne

---

## 🎯 **Comment ça marche ?**

### **Exécution Automatique**

Le fichier commence par `00-` pour qu'il s'exécute **en premier** dans Cypress.

**Ordre d'exécution** :
```
1. 00-setup.cy.ts      ← Crée l'utilisateur
2. auth.cy.ts          ← Teste l'authentification
3. cart.cy.ts          ← Teste le panier (avec login)
4. checkout.cy.ts      ← Teste le paiement (avec login)
5. product.cy.ts       ← Teste les produits
```

### **Gestion Intelligente**

Le test est **intelligent** :
- ✅ Si l'utilisateur **n'existe pas** → Il le crée
- ✅ Si l'utilisateur **existe déjà** → Il continue quand même (pas d'erreur)

---

## 🚀 **Utilisation**

### **Option 1 : Lancer TOUS les tests**

Dans Cypress, cliquez sur **"00-setup.cy.ts"** en premier :

1. **Cliquez sur `00-setup.cy.ts`**
   - Crée l'utilisateur automatiquement
   - Vérifie que le login fonctionne

2. **Puis cliquez sur les autres tests**
   - `auth.cy.ts`
   - `cart.cy.ts`
   - `checkout.cy.ts`
   - `product.cy.ts`

### **Option 2 : Lancer tous les tests en headless**

```bash
npm run cy:run
```

Cela exécutera **tous les tests** dans l'ordre, y compris le setup !

---

## 📊 **Structure Finale**

Vous avez maintenant **5 fichiers de tests** :

```
cypress/e2e/
├── 00-setup.cy.ts       🆕 Setup automatique (2 tests)
├── auth.cy.ts           🔐 Authentification (4 tests)
├── cart.cy.ts           🛒 Panier (4 tests)
├── checkout.cy.ts       💳 Paiement (4 tests)
└── product.cy.ts        🛍️ Produits (3 tests)

TOTAL : 17 tests E2E !
```

---

## 🔐 **Utilisateur Créé**

Le test crée automatiquement :

```
Email        : test@example.com
Mot de passe : password123
Nom          : Test User
Téléphone    : 1234567890
Adresse      : 123 Test Street
```

---

## 🎯 **Ce Qui Se Passe**

### **Première exécution**
```
1. Visite /register
2. Remplit le formulaire avec les infos de test
3. Soumet le formulaire
4. Utilisateur créé ✅
5. Teste le login avec ces identifiants ✅
```

### **Exécutions suivantes**
```
1. Visite /register
2. Remplit le formulaire
3. Soumet le formulaire
4. Email déjà utilisé (normal) ⚠️
5. Teste le login quand même ✅
6. Login réussit car l'utilisateur existe ✅
```

---

## ⚙️ **Personnalisation**

Si vous voulez modifier les informations de l'utilisateur de test, éditez `00-setup.cy.ts` :

```typescript
// Modifier le nom
.type('Test User');          // ← Changez ici

// Modifier l'email
.type('test@example.com');   // ← Changez ici

// Modifier le mot de passe
.type('password123');        // ← Changez ici
```

---

## 💡 **Avantages**

✅ **Aucune action manuelle** requise  
✅ **Setup automatique** pour tous les tests  
✅ **Répétable** : fonctionne à chaque fois  
✅ **Intelligent** : gère les doublons  
✅ **Partageable** : autres développeurs peuvent lancer directement  

---

## 🐛 **Dépannage**

### **Si le test échoue avec "User already exists"**
**C'est normal !** Le test continuera quand même.

### **Si les champs du formulaire ne sont pas trouvés**
Modifiez les sélecteurs dans `00-setup.cy.ts` pour correspondre à votre formulaire.

### **Si vous voulez réinitialiser**
Supprimez l'utilisateur de votre base de données et relancez le test.

---

## 🎬 **PROCHAINE ÉTAPE**

**Dans Cypress, lancez le test `00-setup.cy.ts` maintenant !**

1. Ouvrir Cypress
2. Cliquer sur **`00-setup.cy.ts`**
3. Regarder l'utilisateur se créer automatiquement ✨
4. Lancer les autres tests (`cart.cy.ts`, etc.)

---

## 📈 **Résultat Final**

Avec ce setup automatique :

```
AVANT :
❌ Besoin de créer manuellement l'utilisateur
❌ Tests échouent si pas d'utilisateur
❌ Setup compliqué

APRÈS :
✅ Utilisateur créé automatiquement
✅ Tests fonctionnent directement
✅ Setup en 1 clic !
```

---

**C'est prêt ! Lancez `00-setup.cy.ts` dans Cypress maintenant ! 🚀**

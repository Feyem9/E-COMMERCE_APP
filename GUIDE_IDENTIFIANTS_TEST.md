# 🔐 Guide des Identifiants de Test

## 📝 **Identifiants de Test Utilisés**

Pour les tests E2E qui nécessitent une authentification, j'ai configuré les identifiants suivants :

### **Identifiants par défaut**
```
Email    : test@example.com
Mot de passe : password123
```

---

## ⚙️ **Comment Ajuster les Identifiants**

### **Option 1 : Modifier dans les fichiers de test**

Si vos vrais identifiants de test sont différents, modifiez la fonction `loginUser()` dans :

#### **`cypress/e2e/cart.cy.ts`**
```typescript
const loginUser = () => {
  cy.visit('/login');
  cy.get('form').should('be.visible');
  
  // 👇 MODIFIER ICI
  cy.get('input[type="email"]').first().clear().type('VOTRE_EMAIL@example.com');
  cy.get('input[type="password"]').first().clear().type('VOTRE_MOT_DE_PASSE');
  
  cy.get('button[type="submit"]').first().click();
  cy.wait(2000);
};
```

#### **`cypress/e2e/checkout.cy.ts`**
```typescript
const loginUser = () => {
  cy.visit('/login');
  cy.get('form').should('be.visible');
  
  // 👇 MODIFIER ICI
  cy.get('input[type="email"]').first().clear().type('VOTRE_EMAIL@example.com');
  cy.get('input[type="password"]').first().clear().type('VOTRE_MOT_DE_PASSE');
  
  cy.get('button[type="submit"]').first().click();
  cy.wait(2000);
};
```

---

### **Option 2 : Utiliser les fixtures**

Vous pouvez aussi utiliser le fichier `cypress/fixtures/users.json` :

#### **1. Modifier `cypress/fixtures/users.json`**
```json
{
  "validUser": {
    "email": "VOS_VRAIS_IDENTIFIANTS@example.com",
    "password": "VOTRE_VRAI_MOT_DE_PASSE",
    "name": "Test User"
  }
}
```

#### **2. Utiliser dans les tests**
```typescript
cy.fixture('users').then((users) => {
  cy.get('input[type="email"]').type(users.validUser.email);
  cy.get('input[type="password"]').type(users.validUser.password);
});
```

---

### **Option 3 : Utiliser les variables d'environnement**

Déjà configuré dans `cypress.config.ts` :

```typescript
env: {
  API_URL: 'http://localhost:5000',
  TEST_USER_EMAIL: 'test@example.com',        // 👈 MODIFIER ICI
  TEST_USER_PASSWORD: 'password123',           // 👈 MODIFIER ICI
}
```

**Utilisation dans les tests** :
```typescript
cy.get('input[type="email"]').type(Cypress.env('TEST_USER_EMAIL'));
cy.get('input[type="password"]').type(Cypress.env('TEST_USER_PASSWORD'));
```

---

## 🎯 **Créer un Utilisateur de Test**

Si vous n'avez pas d'utilisateur de test, voici comment en créer un :

### **Option A : Via l'interface de votre app**
1. Aller sur `http://localhost:4200/register`
2. S'inscrire avec :
   - Email : `test@example.com`
   - Mot de passe : `password123`
3. Utiliser ces identifiants dans les tests

### **Option B : Via votre backend**
Si vous avez accès à votre base de données, créez directement un utilisateur de test.

### **Option C : Via les tests Cypress (recommandé)**
Créer un test qui inscrit un utilisateur avant de se connecter :

```typescript
before(() => {
  // S'inscrire une fois avant tous les tests
  cy.visit('/register');
  cy.get('input[name="email"]').type('test@example.com');
  cy.get('input[name="password"]').type('password123');
  cy.get('button[type="submit"]').click();
});
```

---

## 📋 **Tests Qui Utilisent l'Authentification**

Les tests suivants nécessitent un login :

### **`cart.cy.ts`** (4 tests)
- ✅ `devrait rediriger vers login si non authentifié`
- 🔐 `devrait afficher la page du panier après login`
- 🔐 `devrait permettre de naviguer vers le panier depuis la navbar (si connecté)`
- 🔐 `devrait pouvoir accéder à la page de paiement depuis le panier (si connecté)`

### **`checkout.cy.ts`** (4 tests)
- ✅ `devrait rediriger vers login si non authentifié (page paiement)`
- 🔐 `devrait accéder à la page de paiement après login`
- ✅ `devrait afficher la page de tracking des commandes`
- ✅ `devrait permettre de chercher une commande avec un ID (order tracking)`

**Légende** :
- ✅ = Ne nécessite PAS de login
- 🔐 = Nécessite un login

---

## 🔧 **Dépannage**

### **Problème : "User not found" ou "Invalid credentials"**
**Solution** : Créez l'utilisateur de test dans votre base de données

### **Problème : "Login timeout"**
**Solution** : Augmentez le `cy.wait(2000)` à `cy.wait(5000)` dans `loginUser()`

### **Problème : "Form not found"**
**Solution** : Vérifiez que votre page `/login` a bien un `<form>` visible

---

## 💡 **Commande Cypress Personnalisée (Avancé)**

Vous avez déjà une commande `cy.login()` dans `cypress/support/commands.ts` !

**Utilisation** :
```typescript
// Au lieu de :
loginUser();

// Vous pouvez utiliser :
cy.login('test@example.com', 'password123');
```

---

## 📊 **Impact sur les Tests**

Avec l'authentification configurée :

| Test | Avant | Après |
|------|-------|-------|
| `cart.cy.ts` | ❌ Échoue (pas de login) | ✅ Passe (avec login) |
| `checkout.cy.ts` | ⚠️ Redirige vers login | ✅ Gère la redirection |

---

## ✅ **Checklist Avant de Lancer les Tests**

- [ ] J'ai créé un utilisateur avec email `test@example.com`
- [ ] Le mot de passe est `password123`
- [ ] OU j'ai modifié les identifiants dans les tests
- [ ] Mon serveur backend tourne (`http://localhost:5000`)
- [ ] Mon frontend tourne (`http://localhost:4200`)

---

**Maintenant, relancez vos tests dans Cypress !** 🚀

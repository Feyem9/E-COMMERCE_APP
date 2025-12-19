# 🧪 Guide Rapide: Setup Tests E2E avec Cypress

## Installation (5 minutes)

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

# Installation de Cypress
npm install --save-dev cypress @cypress/schematic

# Initialiser Cypress
npx cypress open
```

## Structure des Fichiers

```
cypress/
├── e2e/
│   ├── auth.cy.ts          # Tests authentification
│   ├── cart.cy.ts          # Tests panier
│   ├── checkout.cy.ts      # Tests paiement
│   └── product.cy.ts       # Tests produits
├── fixtures/
│   └── users.json          # Données de test
└── support/
    ├── commands.ts         # Commandes personnalisées
    └── e2e.ts             # Configuration globale
```

## Tests Prioritaires à Créer

### 1. Test d'Authentification (`cypress/e2e/auth.cy.ts`)

```typescript
describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should register a new user', () => {
    cy.get('[data-test="register-link"]').click();
    
    cy.get('[data-test="name-input"]').type('Test User');
    cy.get('[data-test="email-input"]').type(`test${Date.now()}@example.com`);
    cy.get('[data-test="password-input"]').type('Password123!');
    cy.get('[data-test="contact-input"]').type('1234567890');
    cy.get('[data-test="address-input"]').type('123 Test Street');
    
    cy.get('[data-test="register-button"]').click();
    
    // Vérifier redirection vers login
    cy.url().should('include', '/login');
    cy.contains('Registration successful').should('be.visible');
  });

  it('should login with valid credentials', () => {
    cy.get('[data-test="login-link"]').click();
    
    cy.get('[data-test="email-input"]').type('test@example.com');
    cy.get('[data-test="password-input"]').type('password123');
    cy.get('[data-test="login-button"]').click();
    
    // Vérifier succès
    cy.url().should('include', '/');
    cy.get('[data-test="user-menu"]').should('be.visible');
  });

  it('should show error with invalid credentials', () => {
    cy.get('[data-test="login-link"]').click();
    
    cy.get('[data-test="email-input"]').type('wrong@example.com');
    cy.get('[data-test="password-input"]').type('wrongpassword');
    cy.get('[data-test="login-button"]').click();
    
    cy.contains('Invalid credentials').should('be.visible');
  });

  it('should logout successfully', () => {
    // Login first
    cy.login('test@example.com', 'password123');
    
    cy.get('[data-test="user-menu"]').click();
    cy.get('[data-test="logout-button"').click();
    
    cy.url().should('include', '/login');
  });
});
```

### 2. Test du Panier (`cypress/e2e/cart.cy.ts`)

```typescript
describe('Shopping Cart', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123');
  });

  it('should add product to cart', () => {
    cy.visit('/product');
    
    cy.get('[data-test="product-card"]').first().click();
    cy.get('[data-test="add-to-cart"]').click();
    
    cy.get('[data-test="cart-badge"]').should('contain', '1');
    cy.contains('Added to cart').should('be.visible');
  });

  it('should update quantity in cart', () => {
    cy.visit('/cart');
    
    cy.get('[data-test="quantity-input"]').first().clear().type('3');
    cy.get('[data-test="update-quantity"]').first().click();
    
    cy.get('[data-test="quantity-input"]').first().should('have.value', '3');
    cy.get('[data-test="total-price"]').should('not.contain', '0');
  });

  it('should remove item from cart', () => {
    cy.visit('/cart');
    
    const initialCount = cy.get('[data-test="cart-item"]').its('length');
    
    cy.get('[data-test="remove-item"]').first().click();
    cy.contains('Remove').click(); // Confirmation
    
    cy.get('[data-test="cart-item"]').should('have.length', initialCount - 1);
  });

  it('should clear entire cart', () => {
    cy.visit('/cart');
    
    cy.get('[data-test="clear-cart"]').click();
    cy.contains('Clear Cart').click(); // Confirmation
    
    cy.contains('Your cart is empty').should('be.visible');
  });
});
```

### 3. Test du Checkout (`cypress/e2e/checkout.cy.ts`)

```typescript
describe('Checkout Process', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123');
    cy.addProductToCart(1, 2); // Helper function
  });

  it('should complete checkout successfully', () => {
    cy.visit('/cart');
    
    cy.get('[data-test="checkout-button"]').click();
    
    // Page de paiement
    cy.url().should('include', '/payment');
    
    // Vérifier le résumé
    cy.get('[data-test="order-summary"]').should('be.visible');
    cy.get('[data-test="total-amount"]').should('not.be.empty');
    
    // Proceeder au paiement
    cy.get('[data-test="pay-button"]').click();
    
    // Vérifier redirection vers PayUnit (ou success page)
    cy.url().should('match', /payment|success/);
  });

  it('should show error on payment failure', () => {
    cy.intercept('POST', '**/transaction/payment', {
      statusCode: 400,
      body: { error: 'Payment failed' }
    }).as('paymentRequest');
    
    cy.visit('/cart');
    cy.get('[data-test="checkout-button"]').click();
    cy.get('[data-test="pay-button"]').click();
    
    cy.wait('@paymentRequest');
    cy.contains('Payment failed').should('be.visible');
  });
});
```

### 4. Test de Recherche de Produits (`cypress/e2e/product.cy.ts`)

```typescript
describe('Product Search and Browse', () => {
  it('should search for products', () => {
    cy.visit('/product');
    
    cy.get('[data-test="search-input"]').type('iPhone');
    cy.get('[data-test="search-button"]').click();
    
    cy.get('[data-test="product-card"]').should('have.length.greaterThan', 0);
    cy.get('[data-test="product-name"]').each(($el) => {
      expect($el.text().toLowerCase()).to.include('iphone');
    });
  });

  it('should show product details', () => {
    cy.visit('/product');
    
    cy.get('[data-test="product-card"]').first().click();
    
    cy.get('[data-test="product-name"]').should('be.visible');
    cy.get('[data-test="product-price"]').should('be.visible');
    cy.get('[data-test="product-description"]').should('be.visible');
    cy.get('[data-test="add-to-cart"]').should('be.visible');
  });

  it('should filter by category', () => {
    cy.visit('/product');
    
    cy.get('[data-test="category-filter"]').select('Smartphones');
    
    cy.get('[data-test="product-card"]').should('have.length.greaterThan', 0);
  });
});
```

## Commandes Cypress Personnalisées

**Fichier**: `cypress/support/commands.ts`

```typescript
// Login helper
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-test="email-input"]').type(email);
  cy.get('[data-test="password-input"]').type(password);
  cy.get('[data-test="login-button"]').click();
  cy.url().should('not.include', '/login');
});

// Add to cart helper
Cypress.Commands.add('addProductToCart', (productId: number, quantity: number) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:5000/cart/add',
    body: { product_id: productId, quantity: quantity },
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    }
  });
});

// Type declarations
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      addProductToCart(productId: number, quantity: number): Chainable<void>;
    }
  }
}
```

## Configuration Cypress

**Fichier**: `cypress.config.ts`

```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4200',
    supportFile: 'cypress/support/e2e.ts',
    specPattern: 'cypress/e2e/**/*.cy.ts',
    
    // Screenshots et vidéos
    screenshotOnRunFailure: true,
    video: true,
    videoCompression: 32,
    
    // Timeouts
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    
    // Viewport
    viewportWidth: 1280,
    viewportHeight: 720,
    
    setupNodeEvents(on, config) {
      // Plugins ici
    },
  },
  
  env: {
    API_URL: 'http://localhost:5000',
    TEST_USER_EMAIL: 'test@example.com',
    TEST_USER_PASSWORD: 'password123',
  },
});
```

## Scripts Package.json

```json
{
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:run:chrome": "cypress run --browser chrome",
    "cy:run:firefox": "cypress run --browser firefox",
    "test:e2e": "start-server-and-test start http://localhost:4200 cy:run",
    "test:e2e:dev": "start-server-and-test start http://localhost:4200 cy:open"
  }
}
```

## Utilisation

### Mode Développement (Interface Graphique)
```bash
# Terminal 1: Démarrer l'app
npm start

# Terminal 2: Lancer Cypress
npm run cy:open
```

### Mode CI/CD (Headless)
```bash
npm run test:e2e
```

## Fixtures de Test

**Fichier**: `cypress/fixtures/users.json`

```json
{
  "validUser": {
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  },
  "admin": {
    "email": "admin@example.com",
    "password": "admin123",
    "name": "Admin User"
  }
}
```

## Bonnes Pratiques

1. **Utilisez data-test attributes**
   ```html
   <button data-test="login-button">Login</button>
   ```

2. **Évitez les sélecteurs CSS fragiles**
   ❌ `cy.get('.btn-primary')`
   ✅ `cy.get('[data-test="submit-button"]')`

3. **Utilisez des fixtures pour les données**
   ```typescript
   cy.fixture('users').then((users) => {
     cy.login(users.validUser.email, users.validUser.password);
   });
   ```

4. **Interceptez les requêtes API pour tests stables**
   ```typescript
   cy.intercept('GET', '/api/products', { fixture: 'products.json' });
   ```

5. **Nettoyez l'état entre les tests**
   ```typescript
   beforeEach(() => {
     cy.clearLocalStorage();
     cy.clearCookies();
   });
   ```

## Timeline

- **Jour 1**: Setup Cypress + Tests Auth (4-5h)
- **Jour 2**: Tests Cart + Checkout (4-5h)  
- **Jour 3**: Tests Product + Edge cases (3-4h)

**Total**: ~2-3 jours pour couverture E2E complète

## Résultats Attendus

Après implémentation:
- ✅ ~15-20 tests E2E critiques
- ✅ Couverture des parcours utilisateurs principaux
- ✅ Détection précoce des régressions
- ✅ Confiance accrue pour le déploiement

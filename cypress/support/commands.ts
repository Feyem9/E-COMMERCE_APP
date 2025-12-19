// ***********************************************
// Commandes personnalisées pour Cypress
// ***********************************************

// Commande de login réutilisable
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-test="email-input"]').type(email);
  cy.get('[data-test="password-input"]').type(password);
  cy.get('[data-test="login-button"]').click();
  cy.url().should('not.include', '/login');
});

// Commande pour ajouter un produit au panier
Cypress.Commands.add('addProductToCart', (productId: number, quantity: number) => {
  const token = localStorage.getItem('access_token');
  cy.request({
    method: 'POST',
    url: `${Cypress.env('API_URL')}/cart/add`,
    body: { product_id: productId, quantity: quantity },
    headers: {
      Authorization: `Bearer ${token}`
    },
    failOnStatusCode: false
  });
});

// Type declarations pour TypeScript
declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Commande personnalisée pour se connecter
       * @example cy.login('test@example.com', 'password123')
       */
      login(email: string, password: string): Chainable<void>;
      
      /**
       * Commande personnalisée pour ajouter un produit au panier
       * @example cy.addProductToCart(1, 2)
       */
      addProductToCart(productId: number, quantity: number): Chainable<void>;
    }
  }
}

// Prévenir les erreurs TypeScript
export {};
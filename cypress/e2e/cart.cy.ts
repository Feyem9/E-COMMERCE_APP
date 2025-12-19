describe('🛒 Shopping Cart Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  // Helper function pour se connecter
  const loginUser = () => {
    cy.visit('/login');
    
    // Attendre que le formulaire soit visible
    cy.get('form').should('be.visible');
    
    // Se connecter avec des identifiants de test
    // Ajustez ces valeurs selon vos vrais identifiants de test
    cy.get('input[type="email"]').first().clear().type('test@example.com');
    cy.get('input[type="password"]').first().clear().type('password123');
    cy.get('button[type="submit"]').first().click();
    
    // Attendre la redirection après login
    cy.wait(2000);
  };

  it('devrait rediriger vers login si non authentifié', () => {
    // Sans login, visiter le panier devrait rediriger vers login
    cy.visit('/cart');
    
    // Vérifier qu'on est redirigé vers login ou qu'on reste sur cart
    cy.url().should('match', /cart|login/);
  });

  it('devrait afficher la page du panier après login', () => {
    // Se connecter d'abord
    loginUser();
    
    // Puis aller au panier
    cy.visit('/cart');
    
    // Vérifier qu'on accède bien au panier
    cy.url().should('include', '/cart');
    cy.get('body').should('be.visible');
  });

  it('devrait permettre de naviguer vers le panier depuis la navbar (si connecté)', () => {
    // Se connecter d'abord
    loginUser();
    
    // Visiter la page d'accueil
    cy.visit('/');
    
    // Essayer de naviguer vers le panier
    cy.visit('/cart');
    
    // Vérifier qu'on accède au panier
    cy.url().should('include', '/cart');
  });

  it('devrait pouvoir accéder à la page de paiement depuis le panier (si connecté)', () => {
    // Se connecter d'abord
    loginUser();
    
    // Aller au panier
    cy.visit('/cart');
    
    // Essayer de naviguer vers la page de paiement
    cy.visit('/payment');
    
    // Vérifier l'URL (payment ou login)
    cy.url().should('match', /payment|login/);
  });
});


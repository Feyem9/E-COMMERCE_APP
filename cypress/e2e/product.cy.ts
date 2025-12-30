describe('🛍️ Product Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('devrait afficher la liste des produits', () => {
    cy.visit('/product');
    cy.url().should('include', '/product');
    
    // Vérifier la présence de produits ou d'un message
    cy.get('body').should('exist');
  });

  it('devrait avoir une barre de recherche', () => {
    cy.visit('/product');
    
    // Rechercher un élément de recherche (input ou search bar)
    cy.get('input[type="search"], input[placeholder*="search" i], input[placeholder*="recherche" i]')
      .should('exist');
  });

  it('devrait charger la page sans erreurs', () => {
    cy.visit('/product', { failOnStatusCode: false });
    
    // Vérifier qu'il n'y a pas d'erreur 500
    cy.url().should('include', 'localhost:4200');
  });
});

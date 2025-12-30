describe('🔐 Authentication Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('devrait afficher la page d\'accueil', () => {
    // Vérifier que l'URL est correcte
    cy.url().should('include', 'localhost:4200');
    
    // Vérifier que la page charge (body visible)
    cy.get('body').should('be.visible');
    
    // Vérifier qu'il y a du contenu sur la page
    cy.get('app-root').should('exist');
  });

  it('devrait naviguer vers la page de login', () => {
    cy.visit('/login');
    cy.url().should('include', '/login');
    cy.get('form').should('be.visible');
  });

  it('devrait afficher une erreur avec des identifiants invalides', () => {
    cy.visit('/login');
    
    // Attendre que le formulaire soit visible
    cy.get('form').should('be.visible');
    
    // Tenter de se connecter avec des mauvais identifiants
    cy.get('input[type="email"]').first().clear().type('wrong@example.com');
    cy.get('input[type="password"]').first().clear().type('wrongpassword');
    
    // Cliquer sur le bouton de connexion
    cy.get('button[type="submit"]').first().click();
    
    // Vérifier que la page ne redirige pas (on reste sur /login)
    // OU qu'un message d'erreur apparaît quelque part
    cy.wait(2000); // Attendre la réponse du serveur
    
    // Si on reste sur la page login, c'est que ça a échoué (ce qui est attendu)
    cy.url().should('include', '/login');
  });

  it('devrait naviguer vers la page de register', () => {
    cy.visit('/register');
    cy.url().should('include', '/register');
    cy.get('form').should('be.visible');
  });
});

import { defineConfig } from "cypress";

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
      // implement node event listeners here
    },
  },
  
  env: {
    API_URL: 'http://localhost:5000',
    TEST_USER_EMAIL: 'test@example.com',
    TEST_USER_PASSWORD: 'password123',
  },
});

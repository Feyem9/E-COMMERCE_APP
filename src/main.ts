import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';
import * as Sentry from "@sentry/angular";

// ============================================
// CONFIGURATION SENTRY
// ============================================
Sentry.init({
  dsn: "https://ab1615d9a6363e355c6fecb31ef75171@o4510552479498240.ingest.us.sentry.io/4510552482775040",
  
  // Envoyer les données PII par défaut (IP, etc.)
  sendDefaultPii: true,
  
  integrations: [
    // Traçage des transactions
    Sentry.browserTracingIntegration(),
    
    // Replay des sessions (optionnel mais utile)
    Sentry.replayIntegration(),
  ],
  
  // Performance Monitoring (100% des transactions en dev)
  tracesSampleRate: 1.0, // 100% pour dev, mettre 0.5 en production
  
  // Configurer les URLs pour le tracing distribué
  tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
  
  // Session Replay
  replaysSessionSampleRate: 0.1, // 10% des sessions normales
  replaysOnErrorSampleRate: 1.0, // 100% des sessions avec erreurs
  
  // Logs activés
  enableLogs: true,
  
  // Environnement (changer selon le cas)
  environment: "development", // ou "production", "staging"
  
  // Filtrer certaines erreurs (optionnel)
  beforeSend(event) {
    // Ignorer les erreurs de scripts externes
    if (event.exception?.values?.[0]?.value?.includes('Script error')) {
      return null;
    }
    return event;
  },
});

// ============================================
// BOOTSTRAP ANGULAR
// ============================================
platformBrowserDynamic().bootstrapModule(AppModule, {
  ngZoneEventCoalescing: true
})
  .catch(err => {
    console.error(err);
    // Capturer aussi les erreurs de bootstrap
    Sentry.captureException(err);
  });


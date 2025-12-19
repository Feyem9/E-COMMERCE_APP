import { Component } from '@angular/core';
import * as Sentry from "@sentry/angular";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'market';
  
  // ============================================
  // TEST SENTRY
  // ============================================
  public throwTestError(): void {
    // Envoyer un log avant de lancer l'erreur
    Sentry.captureMessage('Test Sentry - Bouton cliqué', 'info');
    
    // Lancer une erreur de test
    throw new Error("🎉 Sentry Test Error - Ça fonctionne !");
  }
}


# 🔧 INSTALLATION SENTRY - Guide Rapide

## 📦 **Étape 1 : Installation (5 min)**

### **Installer les packages**
```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP

npm install --save @sentry/angular @sentry/tracing
```

---

## ⚙️ **Étape 2 : Configuration (10 min)**

### **1. Créer un compte Sentry (gratuit)**

1. Aller sur [sentry.io](https://sentry.io)
2. S'inscrire (gratuit jusqu'à 5000 erreurs/mois)
3. Créer un nouveau projet Angular
4. **Copier votre DSN** (ressemble à : `https://xxxxx@o12345.ingest.sentry.io/12345`)

---

### **2. Configurer dans Angular**

**Fichier : `src/main.ts`**

Ajouter au début du fichier :

```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import * as Sentry from "@sentry/angular";

// CONFIGURATION SENTRY
Sentry.init({
  dsn: "VOTRE_DSN_ICI", // 👈 Remplacer par votre DSN
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  
  // Performance Monitoring
  tracesSampleRate: 0.5, // 50% des transactions
  
  // Session Replay
  replaysSessionSampleRate: 0.1, // 10% des sessions
  replaysOnErrorSampleRate: 1.0, // 100% des erreurs
  
  // Environnement
  environment: "production", // ou "development"
});

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
```

---

### **3. Ajouter ErrorHandler (Optionnel mais recommandé)**

**Fichier : `src/app/app.config.ts`**

Ajouter :

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration } from '@angular/platform-browser';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ErrorHandler } from '@angular/core';
import * as Sentry from "@sentry/angular";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideClientHydration(),
    provideHttpClient(withFetch()),
    provideAnimationsAsync(),
    
    // SENTRY ERROR HANDLER
    {
      provide: ErrorHandler,
      useValue: Sentry.createErrorHandler({
        showDialog: false, // Ne pas montrer le dialogue
      }),
    },
  ]
};
```

---

## ✅ **Étape 3 : Tester (5 min)**

### **1. Forcer une erreur de test**

Créer un bouton temporaire dans votre app :

```typescript
// Dans n'importe quel component
testSentry() {
  throw new Error("Sentry Test Error - Ça marche ! 🎉");
}
```

### **2. Vérifier dans Sentry**

1. Cliquer sur le bouton
2. Aller sur [sentry.io](https://sentry.io)
3. Voir l'erreur apparaître dans votre dashboard ! ✅

---

## 🎯 **Configuration Avancée (Optionnel)**

### **Capturer des informations utilisateur**

```typescript
import * as Sentry from "@sentry/angular";

// Après login
Sentry.setUser({ 
  email: "user@example.com",
  id: "user123"
});

// Avant logout
Sentry.setUser(null);
```

### **Tags personnalisés**

```typescript
Sentry.setTag("page_locale", "fr-FR");
Sentry.setTag("user_type", "premium");
```

### **Contexte additionnel**

```typescript
Sentry.setContext("shopping_cart", {
  items: 3,
  total: 125.50
});
```

---

## 📊 **Ce que Sentry va capturer**

### **Automatiquement** ✅
- Erreurs JavaScript
- Erreurs de réseau (HTTP)
- Promesses non gérées
- Stack traces complets
- Contexte navigateur
- URL de la page

### **Avec configuration** ⚙️
- Performance (temps de chargement)
- Session Replay (vidéo des sessions)
- Breadcrumbs (actions utilisateur)
- Données utilisateur

---

## 💡 **Avantages**

### **Avant Sentry** ❌
```
User: "L'app plante !"
Vous: "Où ? Quand ? Comment ?"
User: "Je sais pas..."
Vous: 😰
```

### **Avec Sentry** ✅
```
Sentry: "Erreur à 14h23 sur /payment"
Sentry: "User ID: 123, Email: john@example.com"
Sentry: "Stack trace: line 45, cart.component.ts"
Vous: "Corrigé en 5 minutes !" 🎉
```

---

## 🚨 **Alertes**

### **Configurer les alertes email**

1. Aller dans Sentry → **Alerts**
2. Créer une règle :
   - "Envoyer email si plus de 10 erreurs en 5 min"
   - "Envoyer email pour toute nouvelle erreur"

### **Intégration Slack (Bonus)**

1. Sentry → **Integrations** → Slack
2. Recevoir les erreurs directement dans Slack ! 📱

---

## 📈 **Dashboard Sentry**

Ce que vous verrez :

```
📊 Sentry Dashboard
├── 🔴 Errors (erreurs par jour)
├── 📈 Performance (temps de réponse)
├── 👥 Users affected (utilisateurs impactés)
├── 🎥 Session Replays (vidéos des bugs)
└── 📱 Releases (versions déployées)
```

---

## ✅ **Checklist Installation**

- [ ] Compte Sentry créé
- [ ] Packages npm installés (`@sentry/angular`)
- [ ] DSN copié
- [ ] Configuration dans `main.ts`
- [ ] ErrorHandler dans `app.config.ts`
- [ ] Test d'erreur fait
- [ ] Erreur visible dans Sentry dashboard

**Si 7/7 ✅ → Sentry opérationnel !**

---

## 🎯 **Temps Total**

- Installation : 5 min
- Configuration : 10 min
- Test : 5 min

**Total : ~20 minutes** ⏱️

---

## 🚀 **Prochaine Étape Après Sentry**

Une fois Sentry installé :

1. ✅ **Google Analytics** (tracking utilisateurs)
2. ✅ **Rate Limiting** (sécurité backend)
3. ✅ **Tests de charge** (K6)

→ Voir `LA_SUITE.md` pour le plan complet !

---

## 📞 **Support**

**Problème ?** Questions fréquentes :

### **"Je ne vois pas mon DSN"**
→ Sentry → Settings → Projects → Votre projet → Client Keys (DSN)

### **"Les erreurs n'apparaissent pas"**
→ Vérifier que l'environnement n'est pas "test" ou "development" avec un filtre

### **"Trop d'erreurs !"**
→ Configurer `beforeSend` pour filtrer :
```typescript
Sentry.init({
  dsn: "...",
  beforeSend(event) {
    // Ignorer certaines erreurs
    if (event.exception?.values?.[0]?.value?.includes('Script error')) {
      return null;
    }
    return event;
  }
});
```

---

**Commencez maintenant ! Dans 20 min, vous aurez le monitoring en place ! 🚀**

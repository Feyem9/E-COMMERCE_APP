# ✅ Préparation Finale - Go-Live Checklist

**Date**: 19 Décembre 2025  
**Objectif**: Vérifications critiques avant production  
**Temps estimé**: 1h30

---

## 1️⃣ **VÉRIFIER MONITORING ACTIF** ✅

### **Sentry - Monitoring d'Erreurs**

#### **A. Configuration Actuelle**

✅ **Sentry est configuré** dans `src/main.ts` :
- DSN: Configuré
- Environment: `development` (⚠️ à changer en `production`)
- Traces Sample Rate: 100% (⚠️ mettre à 50% en prod)
- Session Replay: Actif

#### **B. Actions Requises**

**1. Mettre à jour l'environnement pour production** :

```typescript
// src/main.ts - Ligne 36
environment: "production", // Changer de "development" à "production"
```

**2. Ajuster le sample rate** :

```typescript
// src/main.ts - Ligne 23
tracesSampleRate: 0.5, // 50% en production au lieu de 100%
```

**3. Configurer les URLs de tracking** :

```typescript
// src/main.ts - Ligne 26
tracePropagationTargets: [
  "localhost", 
  "https://market-jet.vercel.app",
  "https://theck-market.onrender.com/api"
],
```

#### **C. Test de Sentry**

**Créer un script de test** :

```bash
# test-sentry.sh
```

```typescript
// Dans la console du navigateur sur staging:
try {
  throw new Error('Test Sentry - Erreur de test');
} catch (error) {
  Sentry.captureException(error);
  console.log('Erreur envoyée à Sentry');
}
```

**Vérifier sur** :
1. Aller sur https://sentry.io/
2. Voir le projet
3. Vérifier que l'erreur de test apparaît

#### **D. Checklist Sentry**

- [x] Sentry installé et configuré
- [ ] Environment = "production"
- [ ] Sample rate = 0.5 (50%)
- [ ] URLs de production configurées
- [ ] Test d'erreur effectué et visible dans Sentry
- [ ] Alertes email configurées

---

## 2️⃣ **TESTER ROLLBACK**

### **A. Préparer le Rollback**

#### **Sur Vercel (Frontend)**

**1. Identifier le dernier déploiement stable** :
- Aller sur https://vercel.com/
- Projet → Deployments
- Noter le deployment ID du dernier stable

**2. Tester le rollback** :

```bash
# Via Vercel CLI
vercel rollback <DEPLOYMENT_ID>

# OU via Dashboard:
# Vercel → Deployments → Previous deployment → "Promote to Production"
```

**3. Automatiser le rollback** :

Créer `scripts/rollback-frontend.sh` :
```bash
#!/bin/bash
# Rollback frontend en cas d'urgence

echo "🔄 Rollback Frontend en cours..."

# Méthode 1: Via Vercel CLI
if command -v vercel &> /dev/null; then
    echo "Utilisation de Vercel CLI..."
    vercel list
    read -p "Entrer le Deployment ID à restaurer: " DEPLOY_ID
    vercel promote $DEPLOY_ID --scope=production
else
    echo "⚠️  Vercel CLI non installé"
    echo "Rollback manuel:"
    echo "1. Aller sur https://vercel.com/"
    echo "2. Deployments → Choisir version stable"
    echo "3. Promote to Production"
fi
```

#### **Sur Render (Backend)**

**1. Via Git Revert** :

```bash
#!/bin/bash
# scripts/rollback-backend.sh

echo "🔄 Rollback Backend en cours..."

cd /home/christian/Bureau/CHRISTIAN/FullStackApp/backend/E-COMMERCE_APP

# Afficher les derniers commits
echo "Derniers commits:"
git log --oneline -5

# Demander quel commit restaurer
read -p "Entrer le hash du commit à restaurer: " COMMIT_HASH

# Revert
git revert $COMMIT_HASH --no-edit

# Push
git push origin master

echo "✅ Rollback effectué. Render va redéployer automatiquement (2-3 min)"
```

**2. Via Render Dashboard** :
- Aller sur https://render.com/
- Service → Manual Deploy
- Choisir un commit précédent

#### **Test de Rollback**

**Scénario de test** :

```bash
# 1. Faire un changement mineur
echo "// Test rollback" >> src/app/app.component.ts

# 2. Commit et deploy
git add .
git commit -m "test: deployment pour tester rollback"
git push origin main

# 3. Attendre déploiement (5 min)

# 4. Effectuer le rollback
git revert HEAD --no-edit
git push origin main

# 5. Vérifier que l'ancienne version est restaurée
```

#### **Checklist Rollback**

- [ ] Script `rollback-frontend.sh` créé
- [ ] Script `rollback-backend.sh` créé
- [ ] Test de rollback frontend effectué
- [ ] Test de rollback backend effectué
- [ ] Temps de rollback mesuré (< 10 min)
- [ ] Procédure documentée

---

## 3️⃣ **PRÉPARER SUPPORT UTILISATEURS**

### **A. Canaux de Support**

#### **1. Email de Support**

**Créer** : `support@market-jet.com` (ou utiliser email existant)

**Template Auto-réponse** :
```
Objet: Confirmation de réception - Support Market

Bonjour,

Merci de nous avoir contactés !

Nous avons bien reçu votre demande et nous vous répondrons dans les 24-48 heures.

Numéro de ticket : #{{TICKET_NUMBER}}

En attendant, consultez notre FAQ : https://market-jet.vercel.app/help

Cordialement,
L'équipe Market
```

#### **2. FAQ - Mise à jour**

Questions fréquentes à ajouter :

```markdown
# FAQ - Foire Aux Questions

## Compte & Connexion

**Q: J'ai oublié mon mot de passe, que faire ?**
R: Cliquez sur "Mot de passe oublié" sur la page de connexion.

**Q: Comment créer un compte ?**
R: Cliquez sur "S'inscrire" et suivez les étapes.

## Commandes & Paiement

**Q: Comment passer une commande ?**
R: 1. Ajoutez des produits au panier
   2. Cliquez sur "Passer commande"
   3. Remplissez vos informations
   4. Validez le paiement

**Q: Quels modes de paiement acceptez-vous ?**
R: Carte bancaire, PayPal, Virement.

**Q: Comment suivre ma commande ?**
R: Connectez-vous → Mon compte → Mes commandes

## Problèmes Techniques

**Q: Le site est lent, que faire ?**
R: 1. Videz le cache de votre navigateur
   2. Essayez en navigation privée
   3. Contactez-nous si le problème persiste

**Q: Je n'arrive pas à me connecter**
R: 1. Vérifiez votre email et mot de passe
   2. Réinitialisez votre mot de passe
   3. Contactez support@market-jet.com
```

#### **3. Runbook - Guide de Dépannage**

**Créer `RUNBOOK.md`** :
```markdown
# Runbook - Guide de Dépannage Production

## Incidents Courants

### 1. Site Down / 500 Error

**Symptômes**: Site inaccessible, erreur 500

**Actions**:
1. Vérifier status Vercel: https://vercel.com/status
2. Vérifier status Render: https://render.com/status
3. Vérifier logs Sentry
4. Rollback si nécessaire

**Temps de résolution**: 5-10 min

### 2. Backend Lent (> 30s)

**Symptômes**: Requêtes API timeout

**Cause**: Cold start Render Free Tier

**Actions**:
1. Attendre que le backend se réveille (30-60s)
2. OU: Upgrade Render plan ($7/mois)
3. OU: Ping régulier toutes les 10 min

### 3. Erreur de Paiement

**Symptômes**: Utilisateurs ne peuvent pas payer

**Actions**:
1. Vérifier logs backend
2. Vérifier API paiement (Stripe/PayPal)
3. Vérifier rate limiting backend

**Escalade**: Contacter support API paiement

### 4. Données Utilisateur Perdues

**Symptômes**: Utilisateurs signalent données manquantes

**Actions**:
1. Vérifier backup base de données
2. Vérifier logs d'accès
3. Restaurer depuis backup si nécessaire

**Temps de résolution**: 15-30 min
```

#### **4. Contact Support d'Urgence**

**Liste des contacts** :

```
Développeur Principal : Christian
Email: christian@market-jet.com
Téléphone: [VOTRE_NUMERO]

Vercel Support:
- Dashboard: https://vercel.com/support
- Email: support@vercel.com

Render Support:
- Dashboard: https://render.com/support
- Email: support@render.com

Sentry:
- Dashboard: https://sentry.io/
- Docs: https://docs.sentry.io/
```

### **Checklist Support Utilisateurs**

- [ ] Email support configuré
- [ ] Template auto-réponse créé
- [ ] FAQ complétée (10+ questions)
- [ ] Runbook créé
- [ ] Contacts d'urgence listés
- [ ] Process d'escalade défini

---

## 4️⃣ **PAGE STATUS/MAINTENANCE**

### **A. Page de Maintenance**

**Créer `src/app/maintenance/maintenance.component.ts`** :

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-maintenance',
  template: `
    <div class="maintenance-container">
      <div class="maintenance-content">
        <i class="fas fa-tools maintenance-icon"></i>
        <h1>🔧 Maintenance en Cours</h1>
        <p class="subtitle">Nous améliorons notre service</p>
        
        <div class="info-box">
          <p><strong>Durée estimée :</strong> 30 minutes</p>
          <p><strong>Retour prévu :</strong> {{ estimatedReturn }}</p>
        </div>
        
        <p class="thank-you">Merci de votre patience ! 🙏</p>
        
        <div class="contact">
          <p>Questions ? Contactez-nous :</p>
          <a href="mailto:support@market-jet.com">support@market-jet.com</a>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .maintenance-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 2rem;
    }
    
    .maintenance-content {
      background: white;
      border-radius: 20px;
      padding: 3rem;
      max-width: 600px;
      text-align: center;
      box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .maintenance-icon {
      font-size: 5rem;
      color: #667eea;
      margin-bottom: 1.5rem;
      animation: spin 2s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    h1 {
      font-size: 2.5rem;
      color: #2d3748;
      margin-bottom: 1rem;
    }
    
    .subtitle {
      font-size: 1.25rem;
      color: #718096;
      margin-bottom: 2rem;
    }
    
    .info-box {
      background: #f7fafc;
      border-radius: 12px;
      padding: 1.5rem;
      margin: 2rem 0;
    }
    
    .info-box p {
      margin: 0.5rem 0;
      font-size: 1.1rem;
    }
    
    .thank-you {
      font-size: 1.2rem;
      margin: 2rem 0;
    }
    
    .contact a {
      color: #667eea;
      text-decoration: none;
      font-weight: 600;
      font-size: 1.1rem;
    }
  `]
})
export class MaintenanceComponent {
  estimatedReturn: string = '18:00';
  
  constructor() {
    // Calculer le retour estimé
    const now = new Date();
    now.setMinutes(now.getMinutes() + 30);
    this.estimatedReturn = now.toLocaleTimeString('fr-FR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  }
}
```

### **B. Page de Status**

**Créer `src/app/status/status.component.ts`** :

```typescript
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface ServiceStatus {
  name: string;
  status: 'operational' | 'degraded' | 'down';
  responseTime?: number;
  lastChecked: Date;
}

@Component({
  selector: 'app-status',
  template: `
    <div class="status-page">
      <h1>📊 État des Services</h1>
      <p class="last-update">Dernière mise à jour : {{ lastUpdate | date:'medium' }}</p>
      
      <div class="services">
        <div *ngFor="let service of services" 
             class="service-card"
             [class.operational]="service.status === 'operational'"
             [class.degraded]="service.status === 'degraded'"
             [class.down]="service.status === 'down'">
          
          <div class="service-header">
            <h3>{{ service.name }}</h3>
            <span class="status-badge" [attr.data-status]="service.status">
              {{ service.status === 'operational' ? '✅ Opérationnel' : 
                 service.status === 'degraded' ? '⚠️ Dégradé' : 
                 '❌ Hors ligne' }}
            </span>
          </div>
          
          <p *ngIf="service.responseTime" class="response-time">
            Temps de réponse : {{ service.responseTime }}ms
          </p>
        </div>
      </div>
      
      <div class="overall-status" *ngIf="allOperational">
        <p>✅ <strong>Tous les systèmes sont opérationnels</strong></p>
      </div>
    </div>
  `,
  styles: [`
    .status-page {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    h1 {
      text-align: center;
      margin-bottom: 1rem;
    }
    
    .last-update {
      text-align: center;
      color: #718096;
      margin-bottom: 2rem;
    }
    
    .services {
      display: grid;
      gap: 1rem;
    }
    
    .service-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
      border-left: 4px solid;
    }
    
    .service-card.operational {
      border-left-color: #48bb78;
    }
    
    .service-card.degraded {
      border-left-color: #ed8936;
    }
    
    .service-card.down {
      border-left-color: #f56565;
    }
    
    .service-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .status-badge {
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
    }
    
    .response-time {
      margin-top: 0.5rem;
      color: #718096;
      font-size: 0.9rem;
    }
    
    .overall-status {
      margin-top: 2rem;
      padding: 1.5rem;
      background: #f0fff4;
      border-radius: 12px;
      text-align: center;
    }
  `]
})
export class StatusComponent implements OnInit {
  services: ServiceStatus[] = [
    {
      name: 'Frontend (Vercel)',
      status: 'operational',
      responseTime: 0,
      lastChecked: new Date()
    },
    {
      name: 'Backend API (Render)',
      status: 'operational',
      responseTime: 0,
      lastChecked: new Date()
    },
    {
      name: 'Base de Données',
      status: 'operational',
      lastChecked: new Date()
    }
  ];
  
  lastUpdate = new Date();
  allOperational = true;
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.checkServices();
    
    // Rafraîchir toutes les 60 secondes
    setInterval(() => this.checkServices(), 60000);
  }
  
  async checkServices() {
    // Test Frontend
    try {
      const t0 = performance.now();
      await this.http.get('https://market-jet.vercel.app').toPromise();
      const t1 = performance.now();
      this.services[0].responseTime = Math.round(t1 - t0);
      this.services[0].status = 'operational';
    } catch (e) {
      this.services[0].status = 'down';
    }
    
    // Test Backend
    try {
      const t0 = performance.now();
      await this.http.get('https://theck-market.onrender.com/product/').toPromise();
      const t1 = performance.now();
      this.services[1].responseTime = Math.round(t1 - t0);
      this.services[1].status = this.services[1].responseTime > 5000 ? 'degraded' : 'operational';
    } catch (e) {
      this.services[1].status = 'down';
    }
    
    this.lastUpdate = new Date();
    this.allOperational = this.services.every(s => s.status === 'operational');
  }
}
```

### **Checklist Page Status/Maintenance**

- [ ] Component `MaintenanceComponent` créé
- [ ] Component `StatusComponent` créé
- [ ] Routes configurées (`/maintenance`, `/status`)
- [ ] Tests des pages effectués
- [ ] Page status accessible publiquement

---

## 📊 **RÉCAPITULATIF - CHECKLIST COMPLÈTE**

### **1. Monitoring** 
- [x] Sentry configuré
- [ ] Environment = production
- [ ] Sample rate ajusté
- [ ] Test d'erreur effectué

### **2. Rollback**
- [ ] Script rollback frontend créé
- [ ] Script rollback backend créé
- [ ] Test rollback effectué
- [ ] Procédure documentée

### **3. Support Utilisateurs**
- [ ] Email support configuré
- [ ] FAQ complétée
- [ ] Runbook créé
- [ ] Contacts listés

### **4. Status/Maintenance**
- [ ] Page maintenance créée
- [ ] Page status créée
- [ ] Tests effectués

---

## 🚀 **PROCHAINE ÉTAPE**

Une fois ces 4 points complétés :

✅ **VOUS ÊTES PRÊT POUR LE GO-LIVE !** 🎉

---

**Créé le**: 19 Décembre 2025  
**Temps estimé**: 1h30  
**Priorité**: CRITIQUE avant production

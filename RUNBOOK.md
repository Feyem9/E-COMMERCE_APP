# 🆘 RUNBOOK - Guide de Dépannage Production

**Date**: 19 Décembre 2025  
**Application**: Market E-Commerce  
**Version**: 1.0.0

---

## 📞 CONTACTS D'URGENCE

### **Équipe Technique**
- **Développeur Principal**: Christian
- **Email**: christian@market-jet.com
- **Téléphone**: [VOTRE_NUMERO]

### **Fournisseurs**
- **Vercel** (Frontend): https://vercel.com/support
- **Render** (Backend): https://render.com/support  
- **Sentry** (Monitoring): https://sentry.io/support

---

## 🚨 INCIDENTS CRITIQUES

### **1. SITE COMPLÈTEMENT DOWN (P0)**

**Symptômes**:
- Site inaccessible (erreur 503/504)
- "This site can't be reached"
- Timeout global

**Diagnostic Rapide**:
```bash
# Test rapide
curl -I https://market-jet.vercel.app
curl -I https://theck-market.onrender.com/product/
```

**Actions Immédiates** (< 5 min):

1. **Vérifier status fournisseurs**:
   - Vercel: https://vercel.com/status
   - Render: https://render.com/status

2. **Si Vercel down** → Attendre (hors de notre contrôle)

3. **Si Render down** → Essayer restart backend:
   ```bash
   # Via Render Dashboard
   - Aller sur https://dashboard.render.com/
   - Service → Manual Deploy → Clear build cache & deploy
   ```

4. **Si problème local** → Rollback:
   ```bash
   cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP
   ./scripts/rollback-frontend.sh
   ```

**Temps de résolution cible**: 5-10 minutes

**Communication**:
- Twitter: "⚠️ Problème technique en cours. Nous travaillons à le résoudre."
- Email: Notification automatique si > 15 min

---

### **2. BACKEND LENT / TIMEOUT (P1)**

**Symptômes**:
- Chargement très lent (> 30s)
- Requêtes API en timeout
- Erreurs 504 Gateway Timeout

**Cause Probable**:
- ⚠️ **Cold Start Render Free Tier** (15 min d'inactivité)

**Actions** (2-3 min):

1. **Attendre 1 minute** (backend se réveille)

2. **Tester manuellement**:
   ```bash
   time curl https://theck-market.onrender.com/product/
   ```

3. **Si temps > 60s** → Backend planté:
   ```bash
   # Redémarrage manuel via Render Dashboard
   - Settings → Manual Deploy
   ```

4. **Solution permanente** (upgrade):
   - Render Paid Plan: $7/mois
   - Élimine cold start

**Temps de résolution**:
- Cold start normal: 30-60s
- Redémarrage manuel: 2-5 min

**Workaround temporaire**:
```bash
# Ping toutes les 10 min (eviter cold start)
# Utiliser un service gratuit comme UptimeRobot
```

---

### **3. ERREUR 500 INTERNE (P1)**

**Symptômes**:
- Erreur 500 sur certaines pages
- "Internal Server Error"

**Actions** (5-10 min):

1. **Vérifier Sentry**:
   - https://sentry.io/
   - Voir les nouvelles erreurs

2. **Analyser l'erreur**:
   - Stack trace
   - Requête qui a planté
   - Données utilisateur (si disponibles)

3. **Fix possible**:
   - Bug code → Rollback
   - Donnée corrompue → Correction manuelle DB
   - API externe down → Attendre

4. **Rollback si nécessaire**:
   ```bash
   ./scripts/rollback-backend.sh
   # OU
   ./scripts/rollback-frontend.sh
   ```

**Temps de résolution**: Variable (5-60 min)

---

### **4. BASE DE DONNÉES CORROMPUE (P0)**

**Symptômes**:
- Erreurs SQLite
- Données utilisateurs perdues
- Impossible de se connecter

**Actions URGENTES** (< 15 min):

1. **NE PAS PANIQUER** - Backup disponible

2. **Identifier l'étendue**:
   - Combien d'utilisateurs affectés?
   - Quelles données manquent?

3. **Restaurer depuis backup**:
   ```bash
   # Si backup automatique Render
   - Render Dashboard → Database → Backups
   - Restaurer le dernier backup stable
   ```

4. **Si pas de backup** → Contacter Render Support IMMEDIAT

**Prévention**:
- ✅ Activer backup automatique quotidien
- ✅ Tester restauration 1x/semaine

---

## ⚠️ INCIDENTS MAJEURS

### **5. PAIEMENT EN ÉCHEC (P1)**

**Symptômes**:
- Utilisateurs ne peuvent pas payer
- Erreurs de transaction
- Timeouts paiement

**Actions** (10-15 min):

1. **Vérifier API paiement** (Stripe/PayPal):
   - Status page
   - Logs d'erreurs

2. **Vérifier rate limiting**:
   ```python
   # Backend - limites actuelles
   # /customer/register: 3/heure
   # /customer/login: 5/minute
   # Ajuster si nécessaire
   ```

3. **Tester manuellement**:
   - Créer transaction test
   - Vérifier log backend

4. **Escalade si nécessaire**:
   - Contacter support API paiement

**Communication utilisateurs**:
"⚠️ Problème temporaire de paiement. Réessayez dans 15 minutes."

---

### **6. ATTAQUE DDoS / TRAFIC ANORMAL (P0)**

**Symptômes**:
- Pics de trafic inhabituels
- Site très lent pour tous
- Logs remplis de même IP

**Actions IMMEDIATES** (< 10 min):

1. **Activer protection Vercel**:
   - Vercel Dashboard → Security
   - Enable DDoS Protection (payant)

2. **Rate Limiting agressif**:
   ```python
   # Backend - réduire limites temporairement
   @limiter.limit("1 per minute")
   ```

3. **Bloquer IPs suspectes**:
   - Via Render → Firewall rules
   - Blacklist IPs

4. **Activer Cloudflare** (si temps):
   - Protection DDoS gratuite
   - CDN + Security

**Escalade**: Contacter Vercel Support URGENT

---

## 📊 INCIDENTS MINEURS

### **7. CSS/UI Cassé**

**Actions**:
1. Vérifier cache navigateur
2. Hard refresh (Ctrl+Shift+R)
3. Si problème persiste → Rollback CSS

**Temps**: 5 min

---

### **8. Lenteur Spécifique**

**Actions**:
1. Lighthouse audit
2. Identifier bottleneck
3. Optimiser code
4. Deploy fix

**Temps**: Variable

---

## 🔧 COMMANDES UTILES

### **Diagnostics Rapides**

```bash
# Test Frontend
curl -I https://market-jet.vercel.app

# Test Backend
curl -I https://theck-market.onrender.com/product/

# Test avec timing
time curl https://market-jet.vercel.app

# Voir logs backend (si accès SSH Render)
render logs --tail

# Rollback rapide
./scripts/rollback-frontend.sh
./scripts/rollback-backend.sh
```

### **Monitoring**

```bash
# Sentry - voir dernières erreurs
open https://sentry.io/

# Vercel - voir déploiements
open https://vercel.com/dashboard

# Render - voir backend
open https://dashboard.render.com/
```

---

## 📋 CHECKLIST POST-INCIDENT

Après résolution d'un incident P0 ou P1:

- [ ] Incident résolu et vérifié
- [ ] Root cause identifiée
- [ ] Documentation mise à jour
- [ ] Users notifiés (si impact > 100)
- [ ] Post-mortem rédigé (si P0)
- [ ] Actions préventives définies
- [ ] Tests ajoutés pour éviter récurrence

---

## 📧 TEMPLATES COMMUNICATION

### **Incident en cours**
```
🚨 INCIDENT EN COURS

L'application rencontre actuellement des difficultés techniques.

Nos équipes travaillent à la résolution.

Durée estimée: [X] minutes

Merci de votre patience.
```

### **Incident résolu**
```
✅ INCIDENT RÉSOLU

L'application est de nouveau opérationnelle.

Nous nous excusons pour la gêne occasionnée.

Si vous rencontrez encore des problèmes, contactez support@market-jet.com
```

---

## 🎯 NIVEAUX DE PRIORITÉ

**P0 - CRITIQUE** 🔴
- Site down complet
- Perte de données
- Sécurité compromise
- **SLA**: < 15 minutes

**P1 - MAJEUR** 🟠  
- Fonctionnalité critique cassée
- Performance dégradée
- **SLA**: < 1 heure

**P2 - MINEUR** 🟡
- Bug UI
- Feature non-critique
- **SLA**: < 4 heures

**P3 - TRIVIAL** 🟢
- Amélioration
- Demande feature
- **SLA**: Best effort

---

**Dernière mise à jour**: 19 Décembre 2025  
**Version**: 1.0.0  
**Maintenu par**: Christian

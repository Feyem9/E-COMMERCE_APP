# 📄 Guide Pages Status & Maintenance

**Date**: 19 Décembre 2025  
**Status**: ✅ Créées et prêtes à l'emploi

---

## 📦 FICHIERS CRÉÉS

| Fichier | Usage | URL |
|---------|-------|-----|
| **maintenance.html** | Page de maintenance | `/maintenance.html` |
| **status.html** | Page de status | `/status.html` |

---

## 🎯 UTILISATION

### **1. Page de Maintenance**

**Quand l'utiliser** :
- Déploiement de nouvelle version
- Maintenance planifiée
- Mise à jour de la base de données
- Correction de bug critique

**Comment activer** :

**Méthode A - Vercel (Recommandé)** :
1. Aller sur Vercel Dashboard
2. Settings → Rewrites
3. Ajouter temporairement :
   ```json
   {
     "source": "/(.*)",
     "destination": "/maintenance.html"
   }
   ```
4. Tous les visiteurs verront la page maintenance

**Méthode B - Fichier de configuration** :
Éditer `vercel.json` temporairement :
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/maintenance.html"
    }
  ]
}
```

**Méthode C - .htaccess (si Apache)** :
```apache
RewriteEngine On
RewriteCond %{REQUEST_URI} !^/maintenance.html$
RewriteRule ^(.*)$ /maintenance.html [R=503,L]
```

**Désactiver** :
- Retirer la règle de rewrite
- Les utilisateurs accèdent à nouveau à l'application

---

### **2. Page de Status**

**Quand l'utiliser** :
- Afficher l'état des services en temps réel
- Lors d'un incident
- Pour transparence utilisateurs

**Comment accéder** :
- URL directe : `https://market-jet.vercel.app/status.html`
- Ajouter un lien dans le footer
- Redirection depuis page d'erreur

**Features** :
- ✅ Check automatique toutes les 60s
- ✅ Affichage temps de réponse
- ✅ Status global (operational/degraded/down)
- ✅ 3 services monitorés:
  - Frontend (Vercel)
  - Backend (Render)
  - Base de données

**Personnalisation** :
Éditer `status.html`, section `services`:
```javascript
const services = [
    {
        name: 'Mon Service',
        url: 'https://example.com',
        description: 'Description du service'
    },
    // Ajouter d'autres services
];
```

---

## 🧪 TESTER LES PAGES

### **Test Local**

```bash
cd /home/christian/Bureau/CHRISTIAN/FullStackApp/frontend/E-COMMERCE_APP/src

# Ouvrir maintenance page
open maintenance.html  # Mac
xdg-open maintenance.html  # Linux
start maintenance.html  # Windows

# Ouvrir status page
open status.html  # Mac
xdg-open status.html  # Linux
start status.html  # Windows
```

### **Test en Production**

Après déploiement sur Vercel :
- **Maintenance** : `https://market-jet.vercel.app/maintenance.html`
- **Status** : `https://market-jet.vercel.app/status.html`

---

## 📋 CHECKLIST

### **Page Maintenance**
- [x] Fichier créé (`src/maintenance.html`)
- [ ] Testé localement
- [ ] Déployé sur Vercel
- [ ] URL vérifiée
- [ ] Temps estimés ajustés

### **Page Status**
- [x] Fichier créé (`src/status.html`)
- [ ] Testé localement
- [ ] Check services fonctionne
- [ ] Auto-refresh testé
- [ ] Déployé sur Vercel

---

## 🎨 PERSONNALISATION

### **Maintenance Page**

**Changer durée estimée** :
Editer ligne ~110 :
```javascript
const returnTime = new Date(now.getTime() + 30 * 60000); // 30 minutes
// Changer 30 pour autre durée
```

**Changer couleurs** :
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Remplacer par vos couleurs */
```

**Changer email support** :
```html
<a href="mailto:support@market-jet.com">support@market-jet.com</a>
<!-- Remplacer par votre email -->
```

### **Status Page**

**Ajouter un service** :
```javascript
const services = [
    // Services existants...
    {
        name: 'Nouveau Service',
        url: 'https://nouveauservice.com',
        description: 'Description'
    }
];
```

**Changer intervalle de refresh** :
Ligne ~280 :
```javascript
setInterval(() => {
    checkAllServices();
}, 60000); // 60 secondes
// Changer 60000 pour autre intervalle (en ms)
```

---

## 🚀 DÉPLOIEMENT

### **Avec Angular (Automatique)**

Les fichiers dans `src/` sont automatiquement copiés lors du build Angular.

```bash
npm run build
# Les fichiers seront dans dist/market/browser/
```

### **Vérification après déploiement**

```bash
# Test maintenance page
curl -I https://market-jet.vercel.app/maintenance.html

# Test status page
curl -I https://market-jet.vercel.app/status.html

# Les deux devraient retourner 200 OK
```

---

## 💡 BONNES PRATIQUES

### **Page Maintenance**

✅ **À faire** :
- Annoncer la maintenance à l'avance (email, réseaux sociaux)
- Estimer temps réaliste (+20% de marge)
- Tester la page avant de l'activer
- Mettre email de support visible

❌ **À éviter** :
- Activer sans prévenir
- Sous-estimer le temps
- Page trop technique (rester simple)

### **Page Status**

✅ **À faire** :
- Afficher lien dans footer
- Mettre à jour pendant incidents
- Garder historique des incidents (optionnel)
- Auto-refresh actif

❌ **À éviter** :
- Fausses informations
- Oublier de mettre à jour
- Check trop fréquent (charge serveur)

---

## 📧 COMMUNICATION

### **Avant Maintenance**

**Email** (J-1) :
```
Objet: 🔧 Maintenance planifiée - Market

Chers utilisateurs,

Une maintenance est prévue demain :
📅 Date : [DATE]
⏰ Heure : [HEURE]
⏱️ Durée estimée : 30 minutes

L'application sera inaccessible pendant ce temps.

Merci de votre compréhension.

L'équipe Market
```

### **Pendant Maintenance**

**Twitter/Facebook** :
```
🔧 Maintenance en cours.
Retour prévu à [HEURE].

Status en temps réel : https://market-jet.vercel.app/status.html
```

### **Après Maintenance**

**Email** :
```
Objet: ✅ Maintenance terminée - Market

L'application est de nouveau en ligne !

Nouvelles fonctionnalités : [LISTE]

Merci de votre patience.
```

---

## 🔗 LIENS UTILES

- **Maintenance page**: `/src/maintenance.html`
- **Status page**: `/src/status.html`
- **Vercel rewrites**: https://vercel.com/docs/concepts/projects/project-configuration#rewrites
- **Uptime monitoring**: https://uptimerobot.com (gratuit)

---

**Créé le**: 19 Décembre 2025  
**Prêt pour production**: ✅ OUI

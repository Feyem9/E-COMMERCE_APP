# 📧 Templates Email Support

**Date**: 19 Décembre 2025  
**Usage**: Réponses standardisées support client

---

## 1. AUTO-RÉPONSE (Confirmation de réception)

**Objet**: ✅ Confirmation de réception - Support Market (#{{TICKET_ID}})

```
Bonjour {{NOM_CLIENT}},

Merci de nous avoir contactés !

Nous avons bien reçu votre demande et nos équipes y répondront dans les plus brefs délais.

📋 Numéro de ticket : #{{TICKET_ID}}
📅 Date : {{DATE}}
⏱️ Délai de réponse : 24-48h maximum

En attendant notre réponse, vous pouvez consulter notre FAQ qui répond aux questions les plus fréquentes :
🔗 https://market-jet.vercel.app/help

Cordialement,
L'équipe Market

---
Support : support@market-jet.com
FAQ : https://market-jet.vercel.app/help
Status : https://market-jet.vercel.app/status
```

---

## 2. RÉSOLUTION DE PROBLÈME

**Objet**: ✅ Résolution - Votre demande #{{TICKET_ID}}

```
Bonjour {{NOMCLIENT}},

Suite à votre demande concernant {{SUJET}}, nous avons le plaisir de vous informer que le problème a été résolu.

{{DESCRIPTION_RESOLUTION}}

N'hésitez pas à nous recontacter si vous avez d'autres questions ou si le problème persiste.

Cordialement,
{{NOM_SUPPORT}}
Équipe Support Market

---
Support : support@market-jet.com
```

---

## 3. COMMANDE - Problème

**Objet**: 📦 Re: Votre commande #{{NUM_COMMANDE}}

```
Bonjour {{NOM_CLIENT}},

Concernant votre commande #{{NUM_COMMANDE}}, nous avons bien pris en compte votre demande.

{{DETAILS_SPECIFIQUES}}

Voici les prochaines étapes :
{{PROCHAINES_ETAPES}}

Nous restons à votre disposition pour toute question.

Cordialement,
{{NOM_SUPPORT}}
Équipe Support Market

---
Suivi de commande : https://market-jet.vercel.app/order-tracking
```

---

## 4. REMBOURSEMENT

**Objet**: 💰 Remboursement - Commande #{{NUM_COMMANDE}}

```
Bonjour {{NOM_CLIENT}},

Nous avons bien traité votre demande de remboursement pour la commande #{{NUM_COMMANDE}}.

Détails du remboursement :
- Montant : {{MONTANT}}€
- Mode de paiement original : {{MODE_PAIEMENT}}
- Délai : 5-10 jours ouvrés

Le remboursement apparaîtra sur votre compte bancaire sous le libellé "Market Refund".

Nous nous excusons pour la gêne occasionnée et espérons vous revoir bientôt.

Cordialement,
{{NOM_SUPPORT}}
Équipe Support Market
```

---

## 5. PROBLÈME TECHNIQUE

**Objet**: 🔧 Re: Problème technique

```
Bonjour {{NOM_CLIENT}},

Merci de nous avoir signalé ce problème technique.

Nos équipes techniques ont identifié et corrigé le problème. Voici ce qui s'est passé :

{{EXPLICATION_PROBLEME}}

Ce qui a été fait :
{{ACTIONS_CORRECTIVES}}

Pouvez-vous vérifier que tout fonctionne maintenant ?

Si le problème persiste, merci de nous renvoyer :
- Capture d'écran de l'erreur
- Navigateur utilisé
- Étapes pour reproduire

Cordialement,
{{NOM_SUPPORT}}
Équipe Support Technique Market
```

---

## 6. ESCALADE - Problème complexe

**Objet**: ⚠️ Escalade - Ticket #{{TICKET_ID}}

```
Bonjour {{NOM_CLIENT}},

Votre demande nécessite une expertise supplémentaire.

Nous avons escaladé votre ticket #{{TICKET_ID}} à notre équipe spécialisée qui vous contactera directement dans les 24 heures.

Merci de votre patience et de votre compréhension.

Cordialement,
{{NOM_SUPPORT}}
Équipe Support Market

---
Priorité : HAUTE
SLA : 24 heures
```

---

## 7. FERMETURE - Pas de réponse

**Objet**: 📋 Fermeture automatique - Ticket #{{TICKET_ID}}

```
Bonjour {{NOM_CLIENT}},

N'ayant pas eu de retour de votre part concernant le ticket #{{TICKET_ID}}, nous considérons que votre problème a été résolu.

Ce ticket sera automatiquement fermé dans 48 heures.

Si vous avez besoin d'aide supplémentaire, vous pouvez :
- Répondre à cet email
- Créer un nouveau ticket
- Consulter notre FAQ

Nous restons à votre disposition.

Cordialement,
Équipe Support Market
```

---

## 8. FEEDBACK - Satisfaction

**Objet**: 📊 Votre avis compte! - Ticket #{{TICKET_ID}}

```
Bonjour {{NOM_CLIENT}},

Votre ticket #{{TICKET_ID}} a été résolu.

Votre avis nous aide à améliorer notre service. Pourriez-vous prendre 30 secondes pour répondre à cette question ?

❓ Êtes-vous satisfait de notre support ?
   😊 Très satisfait
   🙂 Satisfait
   😐 Neutre
   🙁 Insatisfait

{{LIEN_SONDAGE}}

Merci et à bientôt sur Market !

Cordialement,
Équipe Market
```

---

## 9. INCIDENT - Communication

**Objet**: 🚨 Incident technique en cours

```
Chers utilisateurs,

Nous rencontrons actuellement des difficultés techniques sur notre plateforme.

Détails :
- Nature : {{TYPE_INCIDENT}}
- Impact : {{IMPACT}}
- Heure de début : {{HEURE}}
- Résolution estimée : {{DUREE}}

Nos équipes techniques travaillent activement à la résolution.

Nous vous tiendrons informés de l'évolution.

Nous nous excusons pour la gêne occasionnée.

L'équipe Market

---
Status en temps réel : https://market-jet.vercel.app/status
```

---

## 10. INCIDENT - Résolution

**Objet**: ✅ Incident résolu

```
Chers utilisateurs,

L'incident technique signalé à {{HEURE_DEBUT}} est maintenant résolu.

Durée totale : {{DUREE}}
Services affectés : {{SERVICES}}

Tous les services fonctionnent normalement.

Nous nous excusons pour la gêne occasionnée et vous remercions de votre patience.

Si vous rencontrez encore des problèmes, contactez support@market-jet.com

Cordialement,
L'équipe Market

---
Post-mortem disponible : {{LIEN_POSTMORTEM}}
```

---

## 📝 NOTES D'UTILISATION

### **Variables à remplacer**

- `{{NOM_CLIENT}}` : Nom du client
- `{{TICKET_ID}}` : Numéro de ticket unique
- `{{NUM_COMMANDE}}` : Numéro de commande
- `{{DATE}}` : Date actuelle
- `{{MONTANT}}` : Montant en euros
- `{{NOM_SUPPORT}}` : Nom de l'agent support
- etc.

### **Ton à adopter**

- ✅ Professionnel mais chaleureux
- ✅ Empathique
- ✅ Clair et concis
- ✅ Positif

### **Délais de réponse**

- Email standard : 24-48h
- Problème technique : 4-8h
- Incident critique : Immédiat
- Remboursement : 5-10 jours

---

**Créé le**: 19 Décembre 2025  
**Maintenu par**: Équipe Support Market

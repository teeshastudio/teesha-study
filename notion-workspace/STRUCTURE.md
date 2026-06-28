# Teesha Study — Espace Notion Complet

> École en ligne · Notion · Marketing · Communication · Solo

---

## Architecture de l'espace

```
🏠 DASHBOARD PRINCIPAL
│
├── 👥 CRM CLIENTS
├── 📚 CATALOGUE DE CONTENUS
├── 📅 CALENDRIER ÉDITORIAL
├── 💰 PIPELINE VENTES
├── 💸 FINANCES
└── ⚙️ MES PROCESS (SOPs)
```

---

## 1. 🏠 DASHBOARD PRINCIPAL

**Page d'accueil** — vue d'ensemble de l'activité.

### Sections à créer (blocs Notion)

| Bloc | Contenu |
|------|---------|
| En-tête | Logo + citation inspirante |
| Vue rapide | Linked view : tâches du jour (filtre date = aujourd'hui) |
| Chiffres clés | Callout : CA du mois · Nouveaux clients · Contenus publiés |
| Liens rapides | Boutons vers chaque section principale |
| Fil d'actualité | Zone de notes hebdo libres |

---

## 2. 👥 CRM CLIENTS

**Base de données** `Clients`

### Propriétés

| Propriété | Type | Valeurs |
|-----------|------|---------|
| Nom | Titre | — |
| Email | Email | — |
| Téléphone | Téléphone | — |
| Statut | Sélect | `Lead` · `Client actif` · `Client inactif` · `VIP` |
| Produit acheté | Relation → Catalogue | — |
| Date d'achat | Date | — |
| Montant payé | Nombre (€) | — |
| Source | Sélect | `Instagram` · `TikTok` · `Bouche à oreille` · `Newsletter` · `Autre` |
| Notes | Texte | — |
| Satisfaction | Sélect | `⭐` · `⭐⭐` · `⭐⭐⭐` · `⭐⭐⭐⭐` · `⭐⭐⭐⭐⭐` |

### Vues à créer

- **Tableau Kanban** groupé par `Statut`
- **Table complète** triée par `Date d'achat` (décroissant)
- **Galerie VIP** filtrée sur `Statut = VIP`
- **Tableau de bord** avec formules : CA total, nb clients actifs

---

## 3. 📚 CATALOGUE DE CONTENUS

**Base de données** `Contenus`

### Propriétés

| Propriété | Type | Valeurs |
|-----------|------|---------|
| Titre | Titre | — |
| Type | Sélect | `Cours en ligne` · `Fiche pratique` · `Template Notion` · `Mini-formation` · `Ressource gratuite` |
| Thématique | Multi-sélect | `Notion` · `Marketing` · `Communication` · `Productivité` · `Business` |
| Statut | Sélect | `Idée` · `En création` · `Prêt` · `Publié` · `Archivé` |
| Prix | Nombre (€) | — |
| Lien de vente | URL | — |
| Lien contenu | URL | (Gumroad, Teachable, etc.) |
| Date de publication | Date | — |
| Nb ventes | Nombre | — |
| CA généré | Formule | `Nb ventes × Prix` |
| Description courte | Texte | — |

### Vues à créer

- **Board** groupé par `Statut` (pipeline de création)
- **Galerie** filtrée sur `Statut = Publié` (vitrine interne)
- **Table** triée par `CA généré` (décroissant)
- **Tableau par thématique**

---

## 4. 📅 CALENDRIER ÉDITORIAL

**Base de données** `Publications`

### Propriétés

| Propriété | Type | Valeurs |
|-----------|------|---------|
| Titre du post | Titre | — |
| Plateforme | Multi-sélect | `Instagram` · `TikTok` · `Newsletter` · `LinkedIn` · `Pinterest` |
| Format | Sélect | `Carrousel` · `Réel` · `Story` · `Post texte` · `Email` · `Vidéo` |
| Thématique | Multi-sélect | (même que Catalogue) |
| Statut | Sélect | `Idée` · `À rédiger` · `En cours` · `Planifié` · `Publié` |
| Date de publication | Date | — |
| Lien vers contenu | Relation → Contenus | (si le post promeut un produit) |
| Texte / Script | Texte long | — |
| Visuels prêts | Case à cocher | — |
| Lien publié | URL | — |
| Nb vues / reach | Nombre | — |

### Vues à créer

- **Calendrier** par `Date de publication`
- **Board** groupé par `Statut`
- **Table** filtrée par plateforme
- **Vue semaine** (filtre : 7 prochains jours)

---

## 5. 💰 PIPELINE VENTES

**Base de données** `Opportunités`

### Propriétés

| Propriété | Type | Valeurs |
|-----------|------|---------|
| Nom prospect | Titre | — |
| Email | Email | — |
| Produit souhaité | Relation → Catalogue | — |
| Étape | Sélect | `Nouveau contact` · `Intéressé` · `Devis envoyé` · `En attente` · `Gagné 🎉` · `Perdu` |
| Valeur estimée | Nombre (€) | — |
| Source | Sélect | (même que CRM) |
| Date premier contact | Date | — |
| Prochaine action | Texte | — |
| Date relance | Date | — |
| Notes | Texte | — |

### Vues à créer

- **Kanban** groupé par `Étape`
- **Table** filtrée sur `Date relance ≤ aujourd'hui` (relances urgentes)
- **Tableau CA prévisionnel**

---

## 6. 💸 FINANCES

**Base de données** `Transactions`

### Propriétés

| Propriété | Type | Valeurs |
|-----------|------|---------|
| Description | Titre | — |
| Type | Sélect | `Revenu` · `Dépense` |
| Catégorie | Sélect | `Vente cours` · `Vente fiche` · `Abonnement outil` · `Pub/Ads` · `Formation` · `Matériel` · `Autre` |
| Montant | Nombre (€) | — |
| Date | Date | — |
| Produit lié | Relation → Catalogue | — |
| Client lié | Relation → Clients | — |
| Reçu / Facture | Fichier | — |

### Vues à créer

- **Table mensuelle** (filtre par mois)
- **Board** groupé par `Type` (Revenus / Dépenses)
- **Graphique** CA par mois (via propriété `Date` groupée)

### Page complémentaire : Tableau de bord financier

Créer une page avec des blocs `Linked view` et des callouts pour afficher :
- CA total du mois
- Dépenses du mois
- Bénéfice net (formule manuelle ou callout mis à jour)
- Objectif mensuel vs réalisé

---

## 7. ⚙️ MES PROCESS (SOPs)

**Page** avec sous-pages pour chaque processus clé.

### Sous-pages à créer

```
⚙️ Mes Process
│
├── 📦 Process : Créer un nouveau cours
├── 📱 Process : Publier sur Instagram
├── 📧 Process : Envoyer une newsletter
├── 🛒 Process : Onboarding nouveau client
├── 🔄 Process : Relance prospects
└── 📊 Process : Bilan mensuel
```

### Template de SOP (pour chaque sous-page)

```
# [Nom du process]

**Fréquence :** hebdo / mensuel / à la demande
**Durée estimée :** X minutes
**Outils utilisés :** Notion · Canva · ...

---

## Étapes

- [ ] Étape 1
- [ ] Étape 2
- [ ] Étape 3

## Ressources utiles
[liens, templates, exemples]

## Notes
```

---

## Ordre de création recommandé

1. Créer les 5 bases de données (Clients, Contenus, Publications, Opportunités, Transactions)
2. Relier les bases entre elles (relations)
3. Créer les vues dans chaque base
4. Construire le Dashboard principal avec des `Linked views`
5. Créer les pages Process
6. Personnaliser les icônes et les couleurs

---

## Relations entre bases de données

```
Clients ←→ Contenus       (produit acheté)
Clients ←→ Transactions   (client lié)
Contenus ←→ Publications  (contenu promu)
Contenus ←→ Opportunités  (produit souhaité)
Contenus ←→ Transactions  (produit lié)
```

---

*Structure créée pour Teesha Study — École en ligne Notion · Marketing · Communication*

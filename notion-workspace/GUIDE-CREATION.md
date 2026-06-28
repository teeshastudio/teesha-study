# Guide de création pas à pas — Teesha Study Notion

> Suis ce guide dans l'ordre pour monter ton espace en ~2h.

---

## Étape 1 — Créer les bases de données (30 min)

Dans Notion, crée une **nouvelle page** pour chaque base :

1. Tape `/database` → choisir `Database – Full page`
2. Nomme-la et ajoute les propriétés du fichier STRUCTURE.md

**Ordre conseillé :**
1. `Contenus` (c'est la base centrale, les autres s'y rattachent)
2. `Clients`
3. `Publications`
4. `Opportunités`
5. `Transactions`

---

## Étape 2 — Créer les relations (10 min)

Dans chaque base, ajoute une propriété de type **Relation** :

| Dans cette base | Propriété | Pointe vers |
|-----------------|-----------|-------------|
| Clients | Produit acheté | Contenus |
| Clients | Transactions | Transactions |
| Publications | Contenu promu | Contenus |
| Opportunités | Produit souhaité | Contenus |
| Transactions | Produit lié | Contenus |
| Transactions | Client lié | Clients |

---

## Étape 3 — Créer les vues (20 min)

Dans chaque base, clique sur `+ Add a view` en haut à gauche.
Crée les vues listées dans STRUCTURE.md pour chaque base.

**Astuce :** pour les filtres de date (ex: "aujourd'hui"), utilise :
`Filter → Date → is → Today`

---

## Étape 4 — Construire le Dashboard (20 min)

1. Crée une page principale nommée `🏠 Teesha Study`
2. Ajoute un **cover** (image bannière) et une **icône**
3. Crée les sections avec des titres `H2`
4. Pour chaque section, ajoute un bloc `Linked view` :
   - Tape `/linked`
   - Sélectionne ta base de données
   - Choisis la vue souhaitée
   - Filtre si besoin (ex: tâches du jour)

---

## Étape 5 — Créer les pages Process (20 min)

1. Crée une page `⚙️ Mes Process`
2. À l'intérieur, crée une sous-page par process
3. Utilise le template SOP du fichier STRUCTURE.md
4. Coche les cases au fur et à mesure quand tu exécutes

---

## Étape 6 — Personnalisation (10 min)

- **Icônes :** clique sur l'icône de chaque page pour la changer (emoji ou image)
- **Couleurs :** dans chaque board/select, attribue une couleur à chaque statut
- **Couvertures :** ajoute des images de couverture à tes pages principales
- **Sidebar :** organise l'ordre des pages dans la barre latérale par drag & drop

---

## Raccourcis Notion utiles

| Action | Raccourci |
|--------|-----------|
| Nouveau bloc | `/` |
| Titre H1/H2/H3 | `/h1` `/h2` `/h3` |
| Callout (encadré) | `/callout` |
| Base de données | `/database` |
| Vue liée | `/linked` |
| Séparateur | `/divider` |
| Case à cocher | `/todo` |
| Bouton | `/button` |

---

## Checklist finale

- [ ] Base `Contenus` créée avec toutes les propriétés
- [ ] Base `Clients` créée avec toutes les propriétés
- [ ] Base `Publications` créée avec toutes les propriétés
- [ ] Base `Opportunités` créée avec toutes les propriétés
- [ ] Base `Transactions` créée avec toutes les propriétés
- [ ] Relations entre bases configurées
- [ ] Vues créées dans chaque base
- [ ] Dashboard principal construit
- [ ] Pages Process créées
- [ ] Personnalisation (icônes, couleurs, covers)

---

*Tu auras un espace 100% opérationnel pour gérer ton école Teesha Study.*

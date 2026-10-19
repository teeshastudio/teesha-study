# Link-in-bio Teesha Studio

Page « lien en bio » qui remplace Beacons : liens, ressources gratuites (lead magnets), boutique et newsletter.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `contenu.js` | **Le seul fichier à modifier** : textes, liens, ressources, produits |
| `index.html` | Mise en page et couleurs |
| `app.js` | Affiche le contenu (ne pas toucher) |
| `logo.png` | *(à ajouter)* ton logo rond. Sans lui, un logo texte s'affiche |

## Modifier le contenu

Ouvre `contenu.js` et :

- **Ajouter un lead magnet** : copie un bloc `{ ... },` dans `ressourcesGratuites`, puis change le titre, la description et le `lien`. Le lien mène à ta page d'inscription (Systeme.io, MailerLite, Brevo, Kit…).
- **Ajouter un produit** : même chose dans `boutique`. Le `lien` est ton lien de paiement (Stripe Payment Link, Gumroad, Systeme.io…).
- **Masquer sans supprimer** : `visible: false`.
- Une section vide (sans aucun élément visible) disparaît toute seule, avec son onglet.

## Connecter la newsletter

Dans ton outil d'emailing, crée un formulaire intégré (« embed » / HTML) et récupère :

1. l'URL après `action="..."` → à coller dans `newsletter.actionFormulaire` ;
2. le nom des champs prénom et email (`name="..."`) → à mettre dans `champNom` et `champEmail`.

## Mettre en ligne (GitHub Pages, gratuit)

1. Sur GitHub : **Settings → Pages**.
2. Source : `Deploy from a branch`, branche `main`, dossier `/ (root)`.
3. La page sera accessible à `https://teeshastudio.github.io/teesha-study/link-in-bio/`.
4. *(Optionnel)* Branche ton propre nom de domaine dans la même page de réglages.

Il ne reste plus qu'à mettre ce lien dans ta bio Instagram et TikTok.

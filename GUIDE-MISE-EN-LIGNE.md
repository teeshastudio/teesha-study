# 🚀 Mettre en ligne le site Teesha Studio (formulaire + CRM)

> Environ 15 minutes · gratuit · à faire une seule fois

Ce que tu obtiens :
- **`https://teesha-studio.netlify.app/`** → le formulaire « Premier contact », public, à mettre en bio Instagram
- **`https://teesha-studio.netlify.app/crm/`** → ton CRM privé (connexion par e-mail + mot de passe)

Chaque formulaire envoyé apparaît **immédiatement** dans le CRM, à l'étape *Nouvelle demande*.

Fichiers du dépôt :
| Dossier | Rôle |
|---------|------|
| `site/` | Le site à mettre en ligne (formulaire, CRM, configuration) |
| `supabase/schema.sql` | La base de données à créer dans Supabase |

---

## Étape 1 · Créer la base de données (Supabase)

1. Ouvre ton projet **TEESHA STUDIO** sur supabase.com.
2. Menu de gauche → **SQL Editor** → **New query**.
3. Copie **tout** le contenu du fichier `supabase/schema.sql`, colle-le, clique **Run**.
4. Tu dois voir *Success. No rows returned*.

## Étape 2 · Créer ton accès au CRM

1. Menu de gauche → **Authentication** → **Users** → **Add user** → **Create new user**.
2. Mets ton e-mail et un mot de passe solide, coche **Auto Confirm User**, valide.
3. Retourne dans **SQL Editor** → **New query**, colle cette ligne en remplaçant l'e-mail par le tien, puis **Run** :

```sql
insert into public.admins (user_id) select id from auth.users where email = 'TON-EMAIL@exemple.com';
```

4. **Sécurité :** **Authentication** → **Sign In / Providers** (ou *Settings*) → désactive **Allow new users to sign up**. Ainsi personne d'autre ne peut se créer un compte.

## Étape 3 · Mettre le site en ligne (Netlify)

1. Sur GitHub, ouvre le dépôt `teesha-study`, branche `claude/relaxed-pasteur-g09a8b` → bouton **Code** → **Download ZIP**, puis décompresse le fichier.
2. Va sur **app.netlify.com/drop** (crée un compte gratuit si besoin).
3. Glisse le dossier **`site`** (et seulement lui) dans la zone.
4. Netlify te donne une adresse au hasard. Pour la changer : **Site configuration** → **Change site name** → `teesha-studio`.

> Ton propre nom de domaine (ex. `teeshastudio.com`) : Netlify → **Domain management** → **Add a domain**, puis suis les instructions.

## Étape 4 · Tester

1. Ouvre ton adresse et remplis le formulaire avec de fausses infos (joins une image pour tester l'envoi de fichiers).
2. Ouvre `/crm/`, connecte-toi : la demande test est dans **Pipeline → Nouvelle demande**.
3. Supprime la demande test (ouvre la fiche → **Supprimer**).

Si l'envoi échoue : vérifie que l'étape 1 s'est bien terminée par *Success*.

## Étape 5 · Publier

- Lien en bio Instagram + sticker « Lien » en story + réponse rapide en DM.
- Story à la une **« Travailler ensemble »**.

---

## À savoir

- **Pause automatique :** la version gratuite de Supabase met le projet en pause après 7 jours sans aucune activité. Dans ce cas, ouvre supabase.com → ton projet → **Restore**. Avec des demandes régulières, ça n'arrive pas.
- **Anciennes réponses Tally :** dans le CRM, bouton **Importer les réponses Tally (CSV)** (export depuis Tally → *Submissions* → *Download CSV*). Les doublons sont ignorés.
- **Modifier le site plus tard :** refais l'étape 3 avec le nouveau dossier `site` (Netlify → *Deploys* → glisser le dossier).
- **Ne partage jamais** la clé *secret* / *service_role* de Supabase, ni le mot de passe de la base.

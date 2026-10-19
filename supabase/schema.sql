-- ============================================================
-- TEESHA STUDIO — base de données du formulaire + CRM
-- À coller UNE FOIS dans Supabase → SQL Editor → New query → Run
-- ============================================================

-- 1. Qui a accès au CRM (toi seule, ajoutée à l'étape 2 du guide)
create table if not exists public.admins (
  user_id uuid primary key references auth.users (id) on delete cascade
);
alter table public.admins enable row level security;

create or replace function public.is_admin()
returns boolean
language sql
security definer
set search_path = public
stable
as $$
  select exists (select 1 from public.admins where user_id = auth.uid());
$$;

create policy "admin lit la liste des admins" on public.admins
  for select to authenticated using (user_id = auth.uid());

-- 2. Contacts : une ligne par demande reçue
create table if not exists public.contacts (
  id             uuid primary key default gen_random_uuid(),
  recu_le        timestamptz not null default now(),
  nom            text not null check (char_length(nom) between 1 and 200),
  email          text not null default '' check (char_length(email) <= 320),
  instagram      text check (char_length(instagram) <= 200),
  tel            text check (char_length(tel) <= 50),
  activite       text check (char_length(activite) <= 500),
  anciennete     text check (char_length(anciennete) <= 100),
  besoin         text[] not null default '{}',
  projet         text check (char_length(projet) <= 5000),
  objectif       text check (char_length(objectif) <= 200),
  objectif_autre text check (char_length(objectif_autre) <= 500),
  blocages       text check (char_length(blocages) <= 5000),
  budget         text check (char_length(budget) <= 100),
  deadline       text check (char_length(deadline) <= 200),
  fichiers       text[] not null default '{}',
  contact_pref   text check (char_length(contact_pref) <= 50),
  source         text check (char_length(source) <= 100),
  source_autre   text check (char_length(source_autre) <= 300),
  -- Suivi (rempli par toi dans le CRM)
  etape          text not null default 'Nouvelle demande',
  priorite       text,
  relance        date,
  notes          text,
  echanges       jsonb not null default '[]'::jsonb,
  origine        text not null default 'Formulaire',
  ref_externe    text unique,
  maj_le         timestamptz
);
create index if not exists contacts_recu_le_idx on public.contacts (recu_le desc);
alter table public.contacts enable row level security;

-- 3. Projets : une ligne par prestation signée
create table if not exists public.projets (
  id          uuid primary key default gen_random_uuid(),
  cree_le     timestamptz not null default now(),
  contact_id  uuid references public.contacts (id) on delete set null,
  titre       text not null default 'Projet',
  statut      text not null default 'À démarrer',
  offres      text[] not null default '{}',
  debut       date,
  livraison   date,
  lien        text,
  total       numeric(10, 2) not null default 0,
  paye        numeric(10, 2) not null default 0,
  moyen       text,
  paye_le     date,
  notes       text,
  avis        boolean not null default false
);
alter table public.projets enable row level security;

-- 4. Droits
-- Le public (le formulaire) peut SEULEMENT ajouter une demande, avec les champs du formulaire.
revoke all on public.contacts from anon;
revoke all on public.projets from anon;
revoke all on public.admins from anon;
grant insert (nom, email, instagram, activite, anciennete, besoin, projet, objectif, objectif_autre,
              blocages, budget, deadline, fichiers, contact_pref, source, source_autre)
  on public.contacts to anon;

create policy "le formulaire ajoute une demande" on public.contacts
  for insert to anon
  with check (etape = 'Nouvelle demande' and origine = 'Formulaire'
              and char_length(email) >= 3
              and coalesce(array_length(besoin, 1), 0) <= 10
              and coalesce(array_length(fichiers, 1), 0) <= 5);

-- Toi (admin connectée) : tout lire, modifier, supprimer.
grant select, insert, update, delete on public.contacts to authenticated;
grant select, insert, update, delete on public.projets to authenticated;

create policy "admin gère les contacts" on public.contacts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "admin gère les projets" on public.projets
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- 5. Fichiers envoyés via le formulaire (logo, idées…) — 10 Mo max, privés
insert into storage.buckets (id, name, public, file_size_limit)
values ('fichiers', 'fichiers', false, 10485760)
on conflict (id) do nothing;

create policy "le formulaire dépose des fichiers" on storage.objects
  for insert to anon
  with check (bucket_id = 'fichiers' and (storage.foldername(name))[1] = 'demandes');

create policy "admin lit les fichiers" on storage.objects
  for select to authenticated using (bucket_id = 'fichiers' and public.is_admin());

create policy "admin supprime les fichiers" on storage.objects
  for delete to authenticated using (bucket_id = 'fichiers' and public.is_admin());

-- 6. Mise à jour en direct du CRM quand une demande arrive
alter publication supabase_realtime add table public.contacts, public.projets;

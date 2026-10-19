/* =========================================================
   TEESHA STUDIO — CONTENU DE LA PAGE
   ---------------------------------------------------------
   C'est le SEUL fichier à modifier au quotidien.
   - Remplace les liens "#" par tes vrais liens.
   - Ajoute / supprime des ressources ou des produits en
     copiant-collant un bloc { ... }, (sans oublier la virgule).
   - Pour masquer un élément sans le supprimer : visible: false
   ========================================================= */

window.TEESHA = {
  profil: {
    nom: "teesha_studio",
    bio: "Notion · Marketing · Communication\nJe t'aide à lancer ta com' sans te perdre (ni t'épuiser).",
  },

  reseaux: [
    { reseau: "instagram", lien: "https://www.instagram.com/teesha_studio/" },
    { reseau: "tiktok", lien: "https://www.tiktok.com/@teesha_studio" },
    // { reseau: "linkedin",  lien: "https://www.linkedin.com/in/..." },
    // { reseau: "pinterest", lien: "https://www.pinterest.fr/..." },
    // { reseau: "email",     lien: "mailto:contact@teesha-studio.fr" },
  ],

  // Gros boutons verts en haut de page
  liensPrincipaux: [
    { titre: "Premier contact — Teesha Studio", sousTitre: "Parlons de ton projet", lien: "https://formulairets.netlify.app/" },
  ],

  // RESSOURCES GRATUITES (lead magnets)
  // lien = ta page d'inscription (Systeme.io, MailerLite, Brevo, Kit...)
  // ou directement le fichier si tu ne demandes pas l'email.
  ressourcesGratuites: [
    {
      emoji: "✅",
      type: "Checklist",
      titre: "Les 10 erreurs de com' quand on débute",
      description: "La checklist pour vérifier ton compte en 15 minutes.",
      bouton: "Je la télécharge",
      lien: "#",
      visible: false, // exemple : passe à true une fois rempli
    },
    {
      emoji: "🗂️",
      type: "Template Notion",
      titre: "Mon calendrier éditorial Notion",
      description: "Planifie tes posts Insta & TikTok au même endroit.",
      bouton: "Je le récupère",
      lien: "#",
      visible: false, // exemple : passe à true une fois rempli
    },
  ],

  // BOUTIQUE (produits payants)
  // lien = ton lien de paiement (Stripe Payment Link, Gumroad, Systeme.io...)
  // prixBarre et badge sont facultatifs (mets "" pour les masquer).
  boutique: [
    {
      emoji: "📓",
      type: "Template Notion",
      titre: "Le Studio Notion",
      description: "Ton espace complet : clients, contenus, calendrier et finances.",
      prix: "29 €",
      prixBarre: "",
      badge: "Best-seller",
      bouton: "Je le veux",
      lien: "#",
      visible: false, // exemple : passe à true une fois rempli
    },
    {
      emoji: "🎓",
      type: "Mini-formation",
      titre: "Ma com' en 7 jours",
      description: "Un plan simple, jour après jour, pour poser les bases de ta communication.",
      prix: "47 €",
      prixBarre: "67 €",
      badge: "Nouveau",
      bouton: "Je découvre",
      lien: "#",
      visible: false, // exemple : passe à true une fois rempli
    },
  ],

  // Bloc newsletter violet "Ta Safe Place Digitale"
  newsletter: {
    titre: "Ta Safe Place Digitale",
    texte: "Je t'envoie mes conseils, ressources et outils pour éviter les erreurs classiques en communication quand on débute.",
    bouton: "Je m'inscris !",
    // Brevo : colle ici l'URL "action" de ton formulaire Brevo
    // (elle ressemble à https://xxxx.sibforms.com/serve/...).
    // Tant que c'est vide, le formulaire affiche un message de test.
    actionFormulaire: "",
    champNom: "PRENOM", // nom de l'attribut prénom dans Brevo (ou FIRSTNAME)
    champEmail: "EMAIL",
    mentionRgpd: "Pas de spam, désinscription en 1 clic.",
  },

  pied: {
    mentionsLegales: "#",
  },
};

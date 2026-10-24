/* Affiche le contenu défini dans contenu.js — pas besoin de modifier ce fichier. */
(function () {
  const C = window.TEESHA;
  const $ = (id) => document.getElementById(id);

  // Crée un élément : el("a", { class: "x", href: "#" }, enfant1, "texte", ...)
  function el(tag, attrs, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === undefined || v === null || v === false) continue;
      n.setAttribute(k, v);
    }
    for (const e of enfants.flat()) {
      if (e === null || e === undefined || e === "") continue;
      n.append(e instanceof Node ? e : document.createTextNode(e));
    }
    return n;
  }

  // Ouvre les liens externes dans un nouvel onglet
  function attrsLien(lien) {
    const externe = /^https?:/.test(lien);
    return { href: lien || "#", target: externe ? "_blank" : null, rel: externe ? "noopener" : null };
  }

  const ICONES = {
    instagram: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.3"/><circle cx="17.6" cy="6.4" r="1.2" fill="currentColor" stroke="none"/></svg>',
    tiktok: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 2h-3.4v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.1a6.3 6.3 0 1 0 5.4 6.3V8.6a8 8 0 0 0 4.7 1.5V6.7a4.7 4.7 0 0 1-4.7-4.7Z"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.5 3a2 2 0 1 1 0 4 2 2 0 0 1 0-4ZM3 8.5h3V21H3V8.5Zm5.5 0h2.9v1.7h.1c.4-.8 1.4-1.9 3.1-1.9 3.3 0 3.9 2.2 3.9 5V21h-3v-6.8c0-1.6 0-3.7-2.3-3.7s-2.6 1.8-2.6 3.6V21h-3V8.5Z"/></svg>',
    pinterest: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.4 1.8-2.4.8 0 1.2.6 1.2 1.4 0 .8-.5 2.1-.8 3.2-.2 1 .5 1.8 1.5 1.8 1.8 0 3.2-1.9 3.2-4.6 0-2.4-1.7-4.1-4.2-4.1-2.9 0-4.6 2.2-4.6 4.4 0 .9.3 1.8.8 2.3l.1.4-.3 1.2c0 .2-.2.3-.4.2-1.3-.6-2.1-2.5-2.1-4 0-3.3 2.4-6.3 6.9-6.3 3.6 0 6.4 2.6 6.4 6 0 3.6-2.3 6.5-5.4 6.5-1.1 0-2.1-.6-2.4-1.2l-.7 2.5c-.2.9-.9 2.1-1.3 2.8A10 10 0 1 0 12 2Z"/></svg>',
    whatsapp: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>',
    email: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2.5" y="4.5" width="19" height="15" rx="3"/><path d="m3 6 9 7 9-7"/></svg>',
  };

  function carte(item, payante) {
    const etiquettes = el("div", { class: "etiquettes" },
      payante ? null : el("span", { class: "etiquette gratuit" }, "Gratuit"),
      item.type ? el("span", { class: "etiquette" }, item.type) : null,
      item.badge ? el("span", { class: "etiquette badge" }, item.badge) : null,
    );
    const prix = payante
      ? el("span", { class: "prix" }, item.prix || "", item.prixBarre ? el("s", {}, item.prixBarre) : null)
      : el("span");
    const carte = el("a", { class: "carte" + (payante ? " payante" : ""), ...attrsLien(item.lien) },
      el("div", { class: "vignette", "aria-hidden": "true" }, item.emoji || "✨"),
      el("div", {},
        etiquettes,
        el("h3", {}, item.titre),
        item.description ? el("p", {}, item.description) : null,
        el("div", { class: "carte-pied" }, prix, el("span", { class: "btn" }, (item.bouton || "Voir") + " →")),
      ),
    );
    return carte;
  }

  function liste(id, items, payante) {
    const cible = $(id);
    const visibles = (items || []).filter((i) => i.visible !== false);
    if (!visibles.length) {
      cible.closest("section").hidden = true;
      const onglet = document.querySelector(`#onglets a[href="#${cible.closest("section").id}"]`);
      if (onglet) onglet.hidden = true;
      return;
    }
    visibles.forEach((i) => cible.append(i.fichier ? carteLeadMagnet(i) : carte(i, payante)));
  }

  // Profil
  $("nom").textContent = C.profil.nom;
  $("bio").textContent = C.profil.bio;
  C.reseaux.forEach((r) => {
    const a = el("a", { ...attrsLien(r.lien), "aria-label": r.reseau });
    a.innerHTML = ICONES[r.reseau] || ICONES.email;
    $("reseaux").append(a);
  });

  // Gros boutons
  C.liensPrincipaux.forEach((l) => {
    $("liens-principaux").append(
      el("a", { class: "lien-principal", ...attrsLien(l.lien) }, l.titre, l.sousTitre ? el("small", {}, l.sousTitre) : null),
    );
  });

  // Portfolio
  const P = C.portfolio;
  if (P && P.lien) {
    const apercus = (P.apercus || []).slice(0, 3);
    $("portfolio").append(el("a", { class: "portfolio", ...attrsLien(P.lien) },
      apercus.length ? el("div", { class: "portfolio-apercus" }, apercus.map((src) => el("img", { src, alt: "", loading: "lazy" }))) : null,
      el("h2", {}, P.titre),
      P.description ? el("p", {}, P.description) : null,
      el("span", { class: "btn" }, P.bouton + " →"),
    ));
  }

  // Boutons secondaires
  (C.liensSecondaires || []).forEach((l) => {
    $("liens-secondaires").append(el("a", { class: "lien-secondaire", ...attrsLien(l.lien) }, l.icone ? el("span", { "aria-hidden": "true" }, l.icone) : null, l.titre));
  });

  const N = C.newsletter;
  const lienConfidentialite = C.pied.mentionsLegales && C.pied.mentionsLegales !== "#"
    ? el("small", {}, el("a", { href: C.pied.mentionsLegales + "#confidentialite" }, "Politique de confidentialité"))
    : null;

  // Formulaire d'inscription Brevo, réutilisé par la newsletter et les lead magnets
  function formulaireInscription({ bouton, mentions, apresEnvoi }) {
    const form = el("form", { class: "inscription", method: "post" },
      el("input", { type: "text", name: N.champNom, placeholder: "Prénom", autocomplete: "given-name", "aria-label": "Prénom" }),
      el("input", { type: "email", name: N.champEmail, placeholder: "Email", autocomplete: "email", required: "", "aria-label": "Email" }),
      el("button", { type: "submit" }, bouton),
      mentions.map((m) => el("small", {}, m)),
      lienConfidentialite ? lienConfidentialite.cloneNode(true) : null,
      // Champs techniques attendus par Brevo (anti-robot + langue)
      el("input", { type: "text", name: "email_address_check", value: "", hidden: "", tabindex: "-1", autocomplete: "off" }),
      el("input", { type: "hidden", name: "locale", value: "fr" }),
      el("input", { type: "hidden", name: "html_type", value: "simple" }),
    );
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector("button");
      btn.disabled = true;
      btn.textContent = "Envoi…";
      try {
        if (N.actionFormulaire) {
          // Brevo ne renvoie pas de réponse lisible depuis une autre page : on envoie et on remercie.
          // isAjax=1 : même envoi que le formulaire intégré officiel de Brevo
          const url = N.actionFormulaire + (N.actionFormulaire.includes("?") ? "&" : "?") + "isAjax=1";
          await fetch(url, { method: "POST", mode: "no-cors", body: new FormData(form) });
        }
        form.replaceWith(apresEnvoi());
      } catch (_) {
        btn.disabled = false;
        btn.textContent = bouton;
        toast("Oups, l'envoi n'a pas marché. Vérifie ta connexion et réessaie.");
      }
    });
    return form;
  }

  // Lead magnet avec fichier : email demandé, puis bouton de téléchargement
  function carteLeadMagnet(item) {
    const zone = el("div", { class: "lm-action" });
    const ouvrir = el("button", { type: "button", class: "btn btn-large" }, (item.bouton || "Je la reçois") + " →");
    ouvrir.addEventListener("click", () => {
      const form = formulaireInscription({
        bouton: "Recevoir " + (item.nomCourt || "la ressource"),
        mentions: ["En la recevant, tu rejoins aussi " + N.titre + ", ma newsletter. Désinscription en 1 clic."],
        apresEnvoi: () => el("div", { class: "lm-merci" },
          el("p", {}, "C'est à toi ! 🎉"),
          el("a", { class: "btn btn-large", href: item.fichier, download: "", target: "_blank", rel: "noopener" }, "Télécharger " + (item.nomCourt || "") + " ↓"),
          el("small", {}, "Imprime-la ou garde-la dans ton téléphone."),
        ),
      });
      zone.replaceChildren(form);
      form.querySelector("input[type=email]").focus();
    });
    zone.append(ouvrir);
    return el("article", { class: "lead-magnet" },
      el("div", { class: "lm-haut" },
        item.couverture ? el("img", { class: "lm-couverture", src: item.couverture, alt: "Aperçu : " + item.titre, loading: "lazy" }) : null,
        el("div", {},
          el("div", { class: "etiquettes" }, el("span", { class: "etiquette gratuit" }, "Gratuit"), item.type ? el("span", { class: "etiquette" }, item.type) : null),
          el("h3", {}, item.titre),
          item.description ? el("p", {}, item.description) : null,
        ),
      ),
      item.points ? el("ul", { class: "lm-points" }, item.points.map((p) => el("li", {}, p))) : null,
      zone,
    );
  }

  liste("liste-gratuit", C.ressourcesGratuites, false);
  liste("liste-boutique", C.boutique, true);

  // Newsletter
  $("bloc-newsletter").append(
    el("h2", {}, N.titre),
    el("p", {}, N.texte),
    formulaireInscription({
      bouton: N.bouton,
      mentions: N.mentionRgpd ? [N.mentionRgpd] : [],
      apresEnvoi: () => el("p", { class: "merci" }, "C'est noté ! Bienvenue dans la Safe Place 💌"),
    }),
  );

  // Pied de page
  $("annee").textContent = new Date().getFullYear();
  if (C.pied.mentionsLegales && C.pied.mentionsLegales !== "#") $("mentions").href = C.pied.mentionsLegales;
  // sinon on retire le lien tant que la page n'est pas prête
  else $("mentions").parentNode.innerHTML = "© " + new Date().getFullYear() + " Teesha Studio";

  // Les onglets n'ont d'intérêt que s'il y a au moins 2 sections
  if (document.querySelectorAll("#onglets a:not([hidden])").length < 2) $("onglets").hidden = true;

  // Partage
  function toast(msg) {
    const t = $("toast");
    t.textContent = msg;
    t.classList.add("visible");
    setTimeout(() => t.classList.remove("visible"), 2200);
  }
  $("partager").addEventListener("click", async () => {
    const data = { title: document.title, url: location.href };
    try {
      if (navigator.share) return await navigator.share(data);
      await navigator.clipboard.writeText(location.href);
      toast("Lien copié !");
    } catch (_) { /* partage annulé */ }
  });

  // Onglet actif selon la section visible
  const onglets = [...document.querySelectorAll("#onglets a")];
  const obs = new IntersectionObserver((entrees) => {
    entrees.forEach((en) => {
      if (!en.isIntersecting) return;
      onglets.forEach((o) => o.classList.toggle("actif", o.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-40% 0px -55% 0px" });
  document.querySelectorAll("section").forEach((s) => obs.observe(s));
})();

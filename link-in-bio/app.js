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
    visibles.forEach((i) => cible.append(carte(i, payante)));
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

  liste("liste-gratuit", C.ressourcesGratuites, false);
  liste("liste-boutique", C.boutique, true);

  // Newsletter
  const N = C.newsletter;
  const form = el("form", { method: "post", action: N.actionFormulaire || null },
    el("input", { type: "text", name: N.champNom, placeholder: "Prénom", autocomplete: "given-name", "aria-label": "Prénom" }),
    el("input", { type: "email", name: N.champEmail, placeholder: "Email", autocomplete: "email", required: "", "aria-label": "Email" }),
    el("button", { type: "submit" }, N.bouton),
    N.mentionRgpd ? el("small", {}, N.mentionRgpd) : null,
  );
  // Champs techniques attendus par Brevo (anti-robot + langue)
  form.append(
    el("input", { type: "text", name: "email_address_check", value: "", hidden: "", tabindex: "-1", autocomplete: "off" }),
    el("input", { type: "hidden", name: "locale", value: "fr" }),
    el("input", { type: "hidden", name: "html_type", value: "simple" }),
  );
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!N.actionFormulaire) {
      form.replaceWith(el("p", { class: "merci" }, "Merci ! (Formulaire de test : connecte Brevo dans contenu.js)"));
      return;
    }
    const bouton = form.querySelector("button");
    bouton.disabled = true;
    bouton.textContent = "Envoi…";
    try {
      // Brevo ne renvoie pas de réponse lisible depuis une autre page : on envoie et on remercie
      // isAjax=1 : même envoi que le formulaire intégré officiel de Brevo
      await fetch(N.actionFormulaire + (N.actionFormulaire.includes("?") ? "&" : "?") + "isAjax=1", { method: "POST", mode: "no-cors", body: new FormData(form) });
      form.replaceWith(el("p", { class: "merci" }, "C'est noté ! Vérifie ta boîte mail pour confirmer ton inscription 💌"));
    } catch (_) {
      bouton.disabled = false;
      bouton.textContent = N.bouton;
      toast("Oups, l'envoi n'a pas marché. Vérifie ta connexion et réessaie.");
    }
  });
  $("bloc-newsletter").append(el("h2", {}, N.titre), el("p", {}, N.texte), form);

  // Pied de page
  $("annee").textContent = new Date().getFullYear();
  if (C.pied.mentionsLegales && C.pied.mentionsLegales !== "#") $("mentions").href = C.pied.mentionsLegales;
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

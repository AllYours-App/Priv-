# Statut : compte Web

Fait :
- WEB-002 : acompte aligné à 30 % / 70 % dans le devis 06 et le contrat 08 (2026-11-21).
- Repo relu le 2026-11-21 : STATUS, tasks.json, 15 fichiers du dossier Suivi (6 sous-dossiers), pas de README. data/done.json absent de Central (data/ ne contient que inbox.json) : aucune tâche à Moi marquée faite. Les statuts ci-dessous viennent du plan de lancement mis à jour le 2026-10-14 : tout ce qui s'est passé depuis n'est pas dans le repo.
- Site vitrine en ligne sur ducoinweb.fr (domaine OVH, DNS Cloudflare, Worker, HTTPS testé). Formulaire Formspree testé, rendez-vous meetergo intégré, mentions légales et confidentialité renseignées, aucun cookie.
- Tests : accueil à 100 partout, contact à 89 en performance et 100 pour le reste.
- Prospection : 3 emails + 2 réponses types (01), script d'appel (02), note de conformité (03), tableau de suivi structuré (04, vide), script Sirene (05).
- Contrats : devis type (06), CGV (07), contrat de prestation avec cession de droits et article L. 221-3 (08). Tous à l'état de projet, pas encore relus par un juriste.
- SEO : guide Google Business Profile / Search Console (09), script appliquer-domaine.py, tableau suivi-seo.xlsx (non rempli).
- Procédures : plan de lancement client à dupliquer (phases 6 à 8), mode d'emploi client (10), panorama des outils (phase 5).

En cours :
- Envoi sur GitHub des fichiers modifiés par appliquer-domaine.py (canonical, og:url, og:image, données structurées, sitemap). Pas confirmé poussé.
- Choix de la cible de prospection (codes NAF) et constitution de la liste. Le script 05 n'a jamais tourné sur l'API réelle.
- Tableau de suivi prospects : 0 ligne saisie, 0 opposition.
- Panorama des outils : prix à confirmer sur les pages des fournisseurs.

Bloqué :
- Fiche Google (WEB-012) : éligibilité confirmée, fiche à créer. Search Console est actif (rapport d'indexation du 2026-11-21 : 11 pages indexées, 20 non indexées, dont 15 redirections).
- WEB-011 : choix A ("sous réserve d'éligibilité"). Repo conforme, reste à modifier le site en ligne (WEB-027, à Moi).

Incohérences relevées (WEB-002, 010, 011, 019 à 025) :
- Acompte 40 % / 60 % (devis, contrat) contre 30 % / 70 % (CGV, plan). Décision à prendre.
- Délai "5 jours" (site, emails, script) contre "5 jours ouvrés" (CGV, devis, contrat).
- Fiche Google promise sans condition sur le site, "si éligible" ailleurs.
- Frais de tiers : devis et CGV disent option A, le contrat laisse A et B ouvertes.
- Emails 01 : variable [Prénom] sans colonne correspondante dans le tableau 04.
- Mode d'emploi client : renvoie à l'article 12 au lieu du 11.
- Plan : 5 pages contre 4 pages publiques, Pages contre Workers, phases 6 à 8 en double, 11 réponses contre 12.

Prochaine étape :
- Décisions tirées du site en ligne : acompte 30 % / 70 %, délai de 5 jours (réponses client sous 5 jours ouvrés), option A pour le domaine. J'aligne les documents du repo : WEB-002 fait (acompte 30 % / 70 % dans 06 et 08), WEB-019 en cours, puis 025, 010, 020.
- WEB-026 fait : plus aucune décision en attente.
- Pousser les fichiers du site sur GitHub, puis Search Console.
- Choisir les codes NAF, lancer 05-liste-sirene.py.
- Mettre en ligne la section Prospection de la politique de confidentialité avant tout premier email.
- Envoyer 03, 06, 07 et 08 à un juriste avant toute signature ou prospection.
- Choisir une plateforme de facturation électronique (réception obligatoire depuis le 2026-09-01).

Mis à jour le : 2026-11-21
Rythme : 1 tâche terminée sur la dernière fenêtre de 5 h

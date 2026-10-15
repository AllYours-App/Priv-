#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Étapes 1.7 et 3.2 : applique l'adresse définitive du site en une commande.

À lancer à la racine du dépôt, après l'achat du domaine (1.10) :
    python3 appliquer-domaine.py https://mondomaine.fr

Pour le site d'un client, ajoute ses coordonnées (sinon ce sont les tiennes qui seraient publiées) :
    python3 appliquer-domaine.py https://domaine-client.fr --nom "Nom du client" --tel +33600000000 --email contact@domaine-client.fr --description "Plombier à Bayonne."
Ajoute --sans-donnees-structurees pour ne pas insérer ce bloc.

Ce que le script fait :
  - robots.txt : ligne Sitemap avec la vraie adresse
  - sitemap.xml : regénéré avec les 4 pages publiques
  - les 4 pages publiques : balise canonical
  - index.html et contact.html : og:url et og:image en adresse absolue
  - index.html : données structurées (ProfessionalService)
  - supprime les commentaires « À REMPLACER »

Les adresses sans .html (/contact) sont utilisées parce que Cloudflare sert contact.html à cette adresse
(visible dans ton rapport PageSpeed). Le script peut être relancé sans créer de doublon.
Aucune dépendance à installer.
"""
import argparse, json, re, sys
from pathlib import Path

PAGES = {  # fichier -> chemin public
    'index.html': '/',
    'contact.html': '/contact',
    'mentions-legales.html': '/mentions-legales',
    'confidentialite.html': '/confidentialite',
}
AVEC_OG = ('index.html', 'contact.html')


def lire(f): return Path(f).read_text(encoding='utf-8')
def ecrire(f, s): Path(f).write_text(s, encoding='utf-8', newline='')


def domaine_valide(arg):
    d = arg.strip().rstrip('/')
    if not re.fullmatch(r'https://[a-z0-9.-]+\.[a-z]{2,}', d):
        sys.exit("Adresse invalide. Format attendu : https://mondomaine.fr (https, sans chemin, sans espace).")
    return d


def balises_page(html, fichier, base):
    url = base + PAGES[fichier]
    # 1. retire les anciens commentaires et balises générées par une exécution précédente
    html = re.sub(r'[ \t]*<!-- À REMPLACER au déploiement[^>]*-->\n', '', html)
    html = re.sub(r'[ \t]*<link rel="canonical"[^>]*>\n', '', html)
    html = re.sub(r'[ \t]*<meta property="og:url"[^>]*>\n', '', html)
    html = re.sub(r'[ \t]*<meta property="og:image" content="[^"]*">\n',
                  f'  <meta property="og:image" content="{base}/assets/og-image.png">\n' if fichier in AVEC_OG else '', html)
    # 2. ajoute canonical (et og:url) juste après la meta description
    ajout = f'  <link rel="canonical" href="{url}">\n'
    if fichier in AVEC_OG:
        ajout += f'  <meta property="og:url" content="{url}">\n'
    html, n = re.subn(r'(  <meta name="description" content="[^"]*">\n)', r'\1' + ajout.replace('\\', '\\\\'), html, count=1)
    if n != 1:
        sys.exit(f"{fichier} : balise meta description introuvable, rien n'a été modifié.")
    return html


def donnees_structurees(html, base, a):
    data = {
        '@context': 'https://schema.org', '@type': 'ProfessionalService',
        'name': a.nom, 'url': base + '/',
        'description': a.description,
        'telephone': a.tel, 'email': a.email,
        'areaServed': {'@type': 'Country', 'name': 'France'},
    }
    bloc = '  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>\n'
    html = re.sub(r'[ \t]*<script type="application/ld\+json">.*?</script>\n', '', html, flags=re.S)
    return html.replace('  <script>document.documentElement.classList.add', bloc + '  <script>document.documentElement.classList.add', 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('domaine', help='adresse définitive, par exemple https://mondomaine.fr')
    ap.add_argument('--nom', default='P-A Ducoin')
    ap.add_argument('--tel', default='+33771717229')
    ap.add_argument('--email', default='ducoin.co@gmail.com')
    ap.add_argument('--description', default='Création de sites vitrines pour professionnels.')
    ap.add_argument('--sans-donnees-structurees', action='store_true')
    a = ap.parse_args()
    base = domaine_valide(a.domaine)
    for f in list(PAGES) + ['robots.txt', 'sitemap.xml']:
        if not Path(f).exists():
            sys.exit(f"{f} introuvable : lance le script à la racine du dépôt.")
    for f in PAGES:
        html = balises_page(lire(f), f, base)
        if f == 'index.html' and not a.sans_donnees_structurees:
            html = donnees_structurees(html, base, a)
        ecrire(f, html)
    ecrire('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n')
    urls = ''.join(f'  <url><loc>{base}{chemin}</loc></url>\n' for chemin in PAGES.values())
    ecrire('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    print(f'Adresse appliquée : {base}')
    print('Fichiers modifiés : ' + ', '.join(list(PAGES) + ['robots.txt', 'sitemap.xml']))
    print('Vérifie avec « git diff », puis envoie sur GitHub.')


if __name__ == '__main__':
    main()

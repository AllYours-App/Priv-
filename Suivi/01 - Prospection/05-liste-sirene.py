#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Étape 2.3 : liste d'entreprises depuis l'API Recherche d'entreprises (Sirene, INSEE).

Le script sort un CSV avec les colonnes du plan (nom, activité, ville, source...).
Les colonnes « Site actuel », « Téléphone » et « Email professionnel » restent vides :
Sirene ne les contient pas, tu les complètes à la main (Google Maps, fiche publique).

Exemples :
  python3 05-liste-sirene.py --naf 43.22A --departement 64 --max 200
  python3 05-liste-sirene.py --naf 56.10A --code-postal 64200 --sortie restaurants-biarritz.csv

Le code NAF s'écrit avec le point (43.22A). Aucune dépendance à installer.
Limite de l'API : 10 000 résultats par recherche au maximum. Resserre par département
ou code postal si la recherche est plus large.
Écart connu : ce script n'a pas pu être testé sur l'API réelle (réseau bloqué là où il a été
écrit). Il a été testé sur une réponse simulée au format attendu. Si l'API renvoie une
erreur, relève le message affiché et corrige les noms de paramètres dans la fonction chercher().
"""
import argparse, csv, json, sys, time, urllib.parse, urllib.request, urllib.error
from datetime import date

API = 'https://recherche-entreprises.api.gouv.fr/search'
SOURCE = "API Recherche d'entreprises (répertoire Sirene, INSEE), Licence Ouverte 2.0"


def chercher(api, params, tentatives=4):
    """Appelle l'API avec reprise en cas de limite de débit (code 429)."""
    url = api + '?' + urllib.parse.urlencode(params)
    for essai in range(tentatives):
        req = urllib.request.Request(url, headers={'User-Agent': 'pa-ducoin-prospection/1.0', 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=30) as rep:
                return json.load(rep)
        except urllib.error.HTTPError as e:
            if e.code == 429 and essai < tentatives - 1:
                time.sleep(2 * (essai + 1))
                continue
            corps = e.read().decode('utf-8', 'replace')[:300]
            sys.exit(f"Erreur de l'API ({e.code}) : {corps}")
        except urllib.error.URLError as e:
            sys.exit(f"Connexion impossible : {e.reason}")


def diffusible(res):
    """Écarte les entreprises dont les données ne sont pas diffusibles."""
    siege = res.get('siege') or {}
    statut = (res.get('statut_diffusion') or siege.get('statut_diffusion') or 'O')
    nom = res.get('nom_complet') or ''
    return statut == 'O' and nom and '[nd]' not in nom.lower()


def ligne(res, aujourdhui):
    siege = res.get('siege') or {}
    return {
        "Nom de l'entreprise": res.get('nom_complet', ''),
        'Activité (code NAF)': res.get('activite_principale') or siege.get('activite_principale', ''),
        'Ville': siege.get('libelle_commune', ''),
        'Code postal': siege.get('code_postal', ''),
        'Département': siege.get('departement', ''),
        'Forme juridique (code)': res.get('nature_juridique', ''),
        'Site actuel': '',
        'Téléphone': '',
        'Email professionnel': '',
        'Source de la donnée': SOURCE,
        'Date de collecte': aujourdhui,
        'SIREN': res.get('siren', ''),
        'SIRET du siège': siege.get('siret', ''),
    }


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--naf', required=True, help='code NAF avec le point, par exemple 43.22A')
    g = a.add_mutually_exclusive_group(required=True)
    g.add_argument('--departement', help='numéro de département, par exemple 64')
    g.add_argument('--code-postal', dest='cp', help='code postal, par exemple 64200')
    a.add_argument('--max', type=int, default=200, help="nombre maximal d'entreprises à écrire (défaut 200)")
    a.add_argument('--sortie', default='prospects-sirene.csv', help='nom du fichier CSV')
    a.add_argument('--api-url', default=API, help="adresse de l'API (pour les tests)")
    o = a.parse_args()

    params = {'activite_principale': o.naf, 'etat_administratif': 'A', 'per_page': 25, 'page': 1}
    if o.departement: params['departement'] = o.departement
    if o.cp: params['code_postal'] = o.cp

    aujourdhui = date.today().strftime('%d/%m/%Y')
    lignes, vus, ecartes = [], set(), 0
    while len(lignes) < o.max:
        data = chercher(o.api_url, params)
        for res in data.get('results', []):
            siren = res.get('siren')
            if siren in vus:
                continue
            vus.add(siren)
            if not diffusible(res):
                ecartes += 1
                continue
            lignes.append(ligne(res, aujourdhui))
            if len(lignes) >= o.max:
                break
        if params['page'] >= (data.get('total_pages') or 0) or not data.get('results'):
            break
        params['page'] += 1
        time.sleep(0.2)  # l'API limite le nombre d'appels par seconde

    if not lignes:
        sys.exit('Aucune entreprise trouvée avec ces critères.')
    # utf-8-sig et point-virgule : le fichier s'ouvre correctement dans Excel en français
    with open(o.sortie, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=';')
        w.writeheader(); w.writerows(lignes)
    print(f"{len(lignes)} entreprises écrites dans {o.sortie} ({ecartes} écartées : données non diffusibles).")


if __name__ == '__main__':
    main()

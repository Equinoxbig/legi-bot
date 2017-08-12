# Importation des librairies
import requests
import json
from html.parser import HTMLParser
import re

# Utilise pour virer l'encodage HTML de certains caracteres (exemple: "A" majuscule accent grave)
html_charset = HTMLParser()


# GET les donnees d'un amendement specifique
def get_amendement(id_amdt):
    URL = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?id=' + id_amdt + '&leg=15&typeRes=doc'
    data = requests.get(URL)

    if data.status_code != 200:
        return 'error'

    response = json.loads(data.text)

    # Parce que faire des objets JSON etait trop complique pour l'AN
    # ils ont fait des strings qu'il faut split avec "|" puis reattribuer
    # chaque index de l'array a sa key selon le schema donne
    # Schema d'un amendement :
    # id|titreDossierLegislatif|urlDossierLegislatif|urlTexteRef|urlCompteRenduRef|dispositif

    amdt = response['data_table'][0].split('|')

    # Clean la description de l'encodage des caracteres et des tags html
    amdt[5] = re.sub(r"\<(.*?)\>", "", amdt[5])
    amdt[5] = html_charset.unescape(amdt[5])

    return {
        'id': amdt[0],
        'dossier': {
            'titre': amdt[1],
            'url': amdt[2],
        },
        'url_texte': amdt[3],
        'url_compte_rendu': amdt[4],
        'description': amdt[5]
    }


# GET la liste des derniers amendements votes
def get_amendements_list():
    URL = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement&leg=15&premierSignataire=true&rows=500&format=html&tri=datedesc&start=1&typeRes=liste'
    data = requests.get(URL)

    if data.status_code != 200:
        return 'error'

    response = json.loads(data.text)

    # Etant donne que quand on fait quelque chose on le finit
    # On retrouve encore et toujours ces magnifiques JSON
    # Cette fois ci le schema est le suivant :
    # id|numInit|titreDossierLegislatif|urlDossierLegislatif|instance|numAmend|urlAmend|designationArticle|designationAlinea|dateDepot|signataires|sort|missionVisee

    for index, result in enumerate(response['data_table']):
        result = result.split('|')

        # Transformation de chaque string en un dictionnaire selon le schema ci-dessus
        response['data_table'][index] = {
            'id': result[0],
            'dossier': {
                'numero': result[1],
                'titre': result[2],
                'url': result[3]
            },
            'type': result[4],
            'amdt': {
                'numero': result[5],
                'url': result[6]
            },
            'article': result[7],
            'alinea': result[8],
            'date_depot': result[9],
            'cosignataire': html_charset.unescape(result[10]),
            'sort': result[11],
            'mission': result[12]
        }

    return response['data_table']

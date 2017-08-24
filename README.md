# Legi-bot

Legi-bot est un bot twitter relayant (dans la mesure du possible) en temps réel les votes de l'assemblée nationale sur twitter
en donnant des informations telles que la date de dépôt, le sort de l'amendement et des liens vers les ressources.

[F.A.Q](https://github.com/Equinoxbig/legi-bot/wiki/F.A.Q)

### Inspiration

* [Accropolis](https://accropolis.fr) - Informations politiques quotidiennes
* [nosdeputes.fr](https://nosdeputes.fr) - Utilisation des onnées de l'assemblée nationale
* [Data Gueule](https://www.youtube.com/user/datagueule) - Travaux sur la démocratie
* [fourtonfish](https://github.com/fourtonfish) - [Code pour les sondages twitter](https://gist.github.com/fourtonfish/5ac885e5e13e6ca33dca9f8c2ef1c46e)

### Pré-requis

Si vous voulez faire tourner une version locale du code, vous aurez besoin de :
* Python 3.X (testé avec 3.4 >)
* pip
* [Tokens twitter](https://gist.github.com/Equinoxbig/99d25d2208ce3a476b49ac5000b07877)
* [rethinkDB](https://rethinkdb.com/docs/guide/python/)

### Installation

Commencez par cloner le repo :
```
git clone git@github.com:Equinoxbig/legi-bot.git
```
allez dans le dossier puis
installez ensuite les packages à l'aide de pip :
```
pip install -r requirements.txt
```

Une fois le tout installé, créez un fichier `credentials.json` et entrez y vos tokens :
```json
{
    "IPHONE_CONSUMER_KEY": "",
    "IPHONE_CONSUMER_SECRET": "",
    "ACCESS_TOKEN": "",
    "ACCESS_TOKEN_SECRET": ""
}
```

### Configuration rethinkDB

Commencez par modifier le fichier `config.json` avec vos paramètres rethinkDB si nécessaire.
Créez une base de données `legibot` et à l'intérieur, une table `amendements`

La structure des objets qui y seront stockés :
```
{
    "alinea": "",
    "amdt": {
      "numero": "",
      "url": ""
    },
    "article": "",
    "cosignataire": "",
    "date_depot": "",
    "description": "",
    "dossier": {
      "numero": "",
      "titre": "",
      "url": ""
    },
    "id": "",
    "mission": "",
    "sort": "",
    "tweet": {
      "date": 0,
      "id": ""
    },
    "type": "",
    "url_compte_rendu": "",
    "url_texte": ""
}
```

## Test

Pour vérifier que tout marche effectuez, à l'intérieur du dossier, la commande :
```
python3 main.py
```

## Déploiement

Pour faire tourner le script en boucle il suffit d'utiliser le fichier bash legibot

## Contribution

N'hésitez pas à contribuer au projet sur GitHub ou à proposer vos idées sur twitter.

## Auteurs

* **Equinoxbig** - *Développement* - [Profil Github](https://github.com/Equinoxbig) - [Profil Twitter](https://twitter.com/Equinoxbig)
* **Arkkos** - *Beta/Test* - [Profil Github](https://github.com/Arkkos) - [Profil Twitter](https://twitter.com/Arkkos1)
* **Million_tom** - *Design twitter* [Profil Twitter](https://twitter.com/million_tom)

Jetez un oeil à la liste de [contributeurs](https://github.com/Equinoxbig/legi-bot/contributors) qui ont participés.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
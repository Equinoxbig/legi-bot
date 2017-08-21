# Import des librairies et modules
from modules import pollster, getter
import time
import sys

# Array stockant tous les tweets a poster
# et objet pour stocker la reponse de twitter
tweets = []
res = {
    'id': None
}


# Execute le cycle du programme
# le parametre "r" represente rethinkDB
def cycle(api, caps_api, r):

    amendements = getter.get_amendements_list()

    for amendement in amendements:
        amd = r.db('legibot').table('amendements').get(amendement['id']).run()

        # Si l'amendement existe, verifier si le sondage a ete poste il y a 24h
        # Si oui > Tag les cosignataires sur twitter
        # Si non > Attendre
        if amd:
            if amd['tweet']['date'] + 86400000 < (time.time() * 1000):
                return

        # Si l'amendement n'existe pas, GET sa description > log dans la db + le tweeter
        else:
            process_amendement(amd=amendement, r=r)

    post_on_twitter(api=api, caps_api=caps_api, r=r)


# Decoupe l'amendement en plusieurs tweets de 130 caracteres
# Recupere la description de l'amendement
# Rajoute ensuite les tweets dans l'array eponyme
def process_amendement(amd, r):
    # GET la description et le lien d'un amendement
    amd_infos = getter.get_amendement(amd['id'])

    # Ajout de donnees a l'objet amd
    amd['description'] = amd_infos['description']
    amd['url_texte'] = amd_infos['url_texte']
    amd['url_compte_rendu'] = amd_infos['url_compte_rendu']

    r.db('legibot').table('amendements').insert(amd).run()


# Boucle postant les tweets
def post_on_twitter(api, caps_api, r):
    while True:
        # Pour eviter les ratelimits et ne pas
        # eteindre le programme instantanement
        time.sleep(60)

        # Poster le tweet puis le supprimer de la liste
        if tweets:
            # Si le tweet doit etre une reponse utiliser id tweet precedent
            if tweets[0]['reply_id']:
                tweets[0]['reply_id'] = res['id']

            # Si le tweet est un sondage
            if tweets[0]['type'] == 'poll':
                res = pollster.tweet_poll(api=api, caps_api=caps_api, text=tweets[0]['content'],
                                          choice1=tweets[0]['choice1'], choice2=tweets[0]['choice2'], reply_id=tweets[0][['reply_id']])

                # Log les infos sur le sondage pour poster 24h plus tard les cosignataires
                r.db('legibot').table('amendements').get(tweets[0]['amd_id']).update({'tweet': {'id': res['id'], 'date': time.time() * 1000}}).run()

            # Ou s'il est un simple texte
            else:
                res = api.statuses.update(status=tweets[0]['content'], in_reply_to_status_id=tweets[0]['reply_id'])

            # Supprime le tweet de l'array
            tweets.pop(0)

        # S'il ne reste plus rien a tweeter, eteindre le programme
        else:
            # Petite attente pour pas refaire toutes les requests dans la seconde
            time.sleep(300)
            sys.exit()

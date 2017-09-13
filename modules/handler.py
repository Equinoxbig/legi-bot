# coding:utf8
# Import des librairies et modules
from modules import pollster, getter
from pyshorteners import Shortener
import time
import sys

# Array stockant tous les tweets a poster
# et objet pour stocker la reponse de twitter
tweets = []
res = {
    'id': None
}
cache = {}

# Utilise pour raccourcir les liens
shortener = Shortener('Isgd')


# Execute le cycle du programme
# le parametre "r" represente rethinkDB
def cycle(api, caps_api, r):

    amendements = getter.get_amendements_list()

    for amendement in amendements:
        amd = r.db('legibot').table('amendements').get(amendement['id']).run()

        # Si l'amendement n'existe pas, GET sa description > log dans la db + le tweeter
        if not amd:
            # Si l'amendement a ete adopte ou rejete (que le choix a ete fait)
            if (amendement['sort'].lower().startswith('rejet')) or (amendement['sort'].lower().startswith('adopt')):
                # ratelimit que je me suis imposé pour pas trop spam le site de l'AN
                time.sleep(5)
                process_amendement(amd=amendement, r=r)

    # Apres avoir check chaque amendement, poster les infos sur twitter
    post_on_twitter(api=api, caps_api=caps_api, r=r)


# Decoupe l'amendement en plusieurs tweets de 130 caracteres
# Recupere la description de l'amendement
# Rajoute ensuite les tweets dans l'array eponyme
def process_amendement(amd, r):
    tweet = []
    desc = []

    # GET la description et le lien d'un amendement
    amd_infos = getter.get_amendement(amd['id'])

    # Ajout de donnees a l'objet amd
    amd['description'] = amd_infos['description']
    amd['url_texte'] = amd_infos['url_texte']
    amd['url_compte_rendu'] = amd_infos['url_compte_rendu']

    r.db('legibot').table('amendements').insert(amd).run()

    amd_to_string = '({}) Dossier - {}\n({}) Amendement {} déposé le {} : {}'.format(
        amd['short_id'], amd['dossier']['titre'], amd['short_id'], amd['amdt']['numero'], amd['date_depot'], amd['sort'])

    tweet = amd_to_string.split('\n')

    # Fusionne infos dossier et infos amendement si possible
    if (len(tweet[0]) + len(tweet[1]) < 129):
        tweet[1] = tweet[0] + '\n' + tweet[1]
        tweet.pop(0)

    """
    # Description de l'amendement (enlevé car trop long)
    # Separer la description en plusieurs tweets
    desc = tweet[len(tweet) - 1].split(' ')
    tweet[len(tweet) - 1] = desc.pop(0)

    for word in desc:
        if (len(tweet[len(tweet) - 1]) + 1 + len(word) < 129):
            tweet[len(tweet) - 1] += ' {}'.format(word)
        elif(len(word) > 0):
            tweet.append(word)
    """
    # Ajouter les liens
    # avec un cache pour pas refaire les meme requests a is.gd

    link_amd = cache[amd['amdt']['url']] if amd['amdt']['url'] in cache else shortener.short(amd['amdt']['url'])
    link_dossier = cache[amd['dossier']['url']] if amd['dossier']['url'] in cache else shortener.short(amd['dossier']['url'])
    link_texte = cache[amd['url_texte']] if amd['url_texte'] in cache else shortener.short(amd['url_texte'])

    tweet.append('({}) Liens :\n- Amendement: {}\n- Dossier: {}\n- Texte: {}'.format(amd['short_id'], link_amd, link_dossier, link_texte))

    cache[amd['amdt']['url']] = link_amd
    cache[amd['dossier']['url']] = link_dossier
    cache[amd['url_texte']] = link_texte

    # Ajouter le tweet a la liste de tweets a poster
    for (index, message) in enumerate(tweet):
        msg = '[{}/{}] | {}'.format(str(index + 1), str(len(tweet) + 1), message)
        to_tweet = {
            'reply_id': True,
            'type': 'text',
            'content': msg,
            'choice1': 'Pour',
            'choice2': 'Contre',
            'amd_id': amd['id']
        }

        if index == 0:
            to_tweet['reply_id'] = False
            tweets.append(to_tweet)

        elif index == (len(tweet) - 1):
            tweets.append(to_tweet)
            tweets.append({
                'reply_id': True,
                'type': 'poll',
                'choice1': 'Pour',
                'choice2': 'Contre',
                'content': '[{}/{}] | ({}) - Qu\'auriez vous voté ?'.format(str(len(tweet) + 1), str(len(tweet) + 1), amd['short_id']),
                'amd_id': amd['id']
            })

        else:
            tweets.append(to_tweet)


# Boucle postant les tweets
def post_on_twitter(api, caps_api, r):
    print('Démarrage de l\'envoi des tweets !')
    while True:
        # Pour eviter les ratelimits twitter (100 req/h)
        time.sleep(120)

        # Poster le tweet puis le supprimer de la liste
        if tweets:

            # Affiche le tweet dans la console pour pouvoir suivre les erreurs
            print('Contenu : {}\nLength : {}'.format(tweets[0]['content'], len(tweets[0]['content'])))

            # Si le tweet doit etre une reponse utiliser id tweet precedent
            if tweets[0]['reply_id']:
                tweets[0]['reply_id'] = res['id']

            # Si le tweet est un sondage
            if tweets[0]['type'] == 'poll':
                res = pollster.tweet_poll(api=api, caps_api=caps_api, text=tweets[0]['content'],
                                          choice1=tweets[0]['choice1'], choice2=tweets[0]['choice2'], reply_id=tweets[0]['reply_id'])

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
            print('Rien à tweet, prochain scan dans 5 minutes !')
            time.sleep(300)
            sys.exit()

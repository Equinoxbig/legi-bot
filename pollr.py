# Code found here : https://gist.github.com/fourtonfish/5ac885e5e13e6ca33dca9f8c2ef1c46e
# Original: https://paste.wuffs.org/raw/160201.220633.4garttu6

from twitter import *
import json
import os

# Guide on how to get your tokens
# The IPHONE key and secret can be found here : https://gist.github.com/shobotch/5160017
# These tokens have to be "official" tokens to spoof the oauth process.
#
# Then on how to get your personnal access token and secret, You have to
# use the PIN based authentication (https://dev.twitter.com/oauth/pin-based) with the IPHONE's
# key and secret You can use : http://npmjs.com/package/twitter-pin-auth to do that
# Then use the token and secret that you get from it by connecting with your "bot" account
# Then store them in a .json file named credentials.json

# Loads the credentials from a json file in order to use them in Oauth
with open('credentials.json') as config_creditentials:
    CREDENTIALS = json.load(config_creditentials)

    ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = CREDENTIALS['ACCESS_TOKEN_SECRET']
    IPHONE_CONSUMER_KEY = CREDENTIALS['IPHONE_CONSUMER_KEY']
    IPHONE_CONSUMER_SECRET = CREDENTIALS['IPHONE_CONSUMER_SECRET']


# Spoofing the requests
class SpoofOAuth(OAuth):
    def __init__(self, *args, **kwargs):
        OAuth.__init__(self, *args, **kwargs)

    def generate_headers(self):
        # note: the X-Twitter fields may not actually be necessary
        hdr = {
            'User-Agent':
            'Twitter-iPhone/6.45 iOS/9.0.2 (Apple;iPhone8,2;;;;;1)',
            'X-Twitter-Client': 'Twitter-iPhone',
            'X-Twitter-API-Version': '5',
            'X-Twitter-Client-Language': 'en',
            'X-Twitter-Client-Version': '6.45',
        }
        return hdr


auth = SpoofOAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                  IPHONE_CONSUMER_KEY, IPHONE_CONSUMER_SECRET)

api = Twitter(auth=auth)
caps_api = Twitter(domain='caps.twitter.com', api_version='v2', auth=auth)


def tweet_poll(text, choice1, choice2):
    # Tweet parameters
    poll_text = text
    poll_card = {
        'twitter:string:choice1_label': choice1,
        'twitter:string:choice2_label': choice2,
        'twitter:long:duration_minutes': 1440,
        'twitter:api:api:endpoint': '1',
        'twitter:card': 'poll2choice_text_only',
    }

    # Generating the poll card from the twitter API before posting it as
    # a tweet parameter
    # https://caps.twitter.com/v2/cards/create.json?card_data=...&send_error_codes=1
    card_data = caps_api.cards.create(
        card_data=json.dumps(poll_card),
        send_error_codes=1)

    # Sending the tweet to twitter using the card generated above
    # https://api.twitter.com/1.1/statuses/update.json?status=...&card_uri=...&cards_platform=iPhone-13&include_cards=1
    api.statuses.update(
        status=poll_text,
        card_uri=card_data['card_uri'],
        cards_platform='iPhone-13',
        include_cards=1)


tweet_poll(text="Ceci est un test", choice1="Test1", choice2="test2")

# Code inspired and based on @fourtonfish's script
# Code can be found here : https://gist.github.com/fourtonfish/5ac885e5e13e6ca33dca9f8c2ef1c46e

# Importing libraries
from twitter import *
import json
import pollster

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
with open('credentials.json') as config_credentials:
    CREDENTIALS = json.load(config_credentials)

    ACCESS_TOKEN = CREDENTIALS['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = CREDENTIALS['ACCESS_TOKEN_SECRET']
    IPHONE_CONSUMER_KEY = CREDENTIALS['IPHONE_CONSUMER_KEY']
    IPHONE_CONSUMER_SECRET = CREDENTIALS['IPHONE_CONSUMER_SECRET']


# Spoofing requests to twitter
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


# Generating "fake" Oauth
auth = SpoofOAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                  IPHONE_CONSUMER_KEY, IPHONE_CONSUMER_SECRET)


# Connecting to APIs
api = Twitter(auth=auth)
caps_api = Twitter(domain='caps.twitter.com', api_version='v2', auth=auth)


# pollster.tweet_poll(api=api,
#                    caps_api=caps_api,
#                    text="Test12",
#                    choice1="Test1",
#                    choice2="Test2")

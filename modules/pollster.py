# still needing json lib
import json


# Function used to tweet a poll taking an twitter API connection
# and a cards API access
def tweet_poll(api, caps_api, text, choice1, choice2):
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
    card_data = caps_api.cards.create(card_data=json.dumps(poll_card), send_error_codes=1)

    # Sending the tweet to twitter using the card generated above
    # using return to get the response object from twitter
    # https://api.twitter.com/1.1/statuses/update.json?status=...&card_uri=...&cards_platform=iPhone-13&include_cards=1
    return api.statuses.update(status=poll_text, card_uri=card_data['card_uri'], cards_platform='iPhone-13', include_cards=1)

import requests
import json

# Get a single amendement


def get_amendement(numAmdt):
    URL = 'http://eliasse.assemblee-nationale.fr/eliasse/amendement.do?_dc=1501455321175&legislature=15&bibard=105&bibardSuffixe=&organeAbrv=AN&numAmdt='
    URL += str(numAmdt)
    data = requests.get(URL)

    if data.status_code != 200:
        return 'error'

    return json.loads(data.text)

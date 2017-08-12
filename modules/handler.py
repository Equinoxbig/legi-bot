from modules import pollster, getter
import time


# Executes a cycle then shuts down
# and waits X seconds to be called again
# r stands for rethinkDB
def cycle(api, caps_api, r):

    # GET LIST_AMENDEMENTS
    # FOREACH AMENDEMENTS GET AMENDEMENT
    # IF KNOWN POLL_ENDED ? TWEET GROUP : WAIT
    # IF UNKNOWN LOG IN DB AND TWEET OUT

    # api.statuses.update(status='Test1!XD', in_reply_to_status_id='892105917747126273')

    amendements = getter.get_amendements_list()

    for amendement in amendements:
        amd = r.db('legibot').table('amendements').get(amendement['id']).run()

        if amd:
            print('amd exists')
        else:
            print('amd doesn\'t exist')

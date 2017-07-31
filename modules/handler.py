# Executes a cycle then shuts down
# and waits X seconds to be called again


def cycle(api, caps_api, db):

    # GET LIST_AMENDEMENTS
    # FOREACH AMENDEMENTS GET AMENDEMENT
    # IF KNOWN POLL_ENDED ? TWEET GROUP : WAIT
    # IF UNKNOWN LOG IN DB AND TWEET OUT

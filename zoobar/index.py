from flask import g, render_template, request
from login import requirelogin
from debug import *
from zoodb import *
import modify_profile_client

@catch_err
@requirelogin
def index():
    try:
        if 'profile_update' in request.form:
            profile = request.form['profile_update']
            modify_profile_client.modify_profile(g.user.person.username, g.user.token, profile)

        g.user.person.profile = modify_profile_client.get_profile(g.user.person.username)

    except (KeyError, ValueError, AttributeError) as e:
        traceback.print_exc()
        warning = "Modify profile failed"

    return render_template('index.html')

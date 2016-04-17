from flask import g, render_template, request, Markup

from login import requirelogin
from zoodb import *
from debug import *
from profile import *
import bank_client
import modify_profile_client
import message_client
import cgi

@catch_err
@requirelogin
def users():
    args = {}
    args['req_user'] = Markup(request.args.get('user', ''))
    if 'user' in request.values:
        persondb = person_setup()
        user = persondb.query(Person).get(request.values['user'])
        if user:
            if 'message' in request.form:
                sender = g.user.person.username
                token = g.user.token
                to = user.username
                message = cgi.escape(request.form['message'])
                message_client.send_message(sender, token, to, message)

            p = modify_profile_client.get_profile(user.username)
            if p.startswith("#!python"):
                p = run_profile(user)

            p_markup = Markup("<b>%s</b>" % p)
            args['profile'] = p_markup

            args['user'] = user
            args['user_zoobars'] = bank_client.balance(user.username)
            args['transfers'] = bank_client.get_log(user.username)
        else:
            args['warning'] = "Cannot find that user."

    return render_template('users.html', **args)

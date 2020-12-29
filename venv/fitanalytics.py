# from fitbit import gather_keys_oauth2 as oauth2  # gather_keys_oauth2.py file needs to be in same directory as main file
import os

from flask import Flask, redirect, url_for, session, request
from flask_dance import OAuth2ConsumerBlueprint
from requests_oauthlib import OAuth2Session

# TODO : Work with OAuth2 Authorization Flow to Hide client_id, client_secret, access_token, refresh_token
# TODO : Get flask to redirect to fitbit authorization login page
# TODO : Get authorization/access tokens working
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_ID = '#####'  # OAuth 2.0 Client ID
CLIENT_SECRET = '#####'
scopes = ["activity ",
          "nutrition ",
          "heartrate ",
          "location ",
          "nutrition ",
          "profile ",
          "settings ",
          "sleep ",
          "social ",
          "weight ",
          ]
scopes2 = ["activity",
           "nutrition",
           "heartrate",
           "location",
           "nutrition",
           "profile",
           "settings",
           "sleep",
           "social",
           "weight",
           ]
lifetime = 604800
authorization_base_url = "https://www.fitbit.com/oauth2/authorize"
# Flask OAuth2 Custom Blueprint for Fitbit API
app = Flask(__name__)
fitbit_blueprint = OAuth2ConsumerBlueprint(
    "fitbit-api", __name__,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    base_url="https://www.fitbit.com",
    token_url="https://api.fitbit.com/oauth2/token",
    authorization_url="https://www.fitbit.com/oauth2/authorize",
    scope=scopes
)
app.secret_key = os.urandom(24)
# app.register_blueprint(fitbit_blueprint, url_prefix="/login")
# app.token = fitbit_blueprint.token
# print(app.token)

print(app.url_map)


@app.route("/")
def index():
    # return redirect(url_for("fitbit-api.login"))
    # return render_template('index.html')
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    fitbit = OAuth2Session(CLIENT_ID)
    # State is used to prevent CSRF, keep this for later.\
    authorization_url, state = fitbit.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    session['scopes'] = scopes
    return redirect(url_for("fitbit-api.login"))
    #redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    fitbit = OAuth2Session(CLIENT_ID, state=session['oauth_state'])
    token = fitbit.fetch_token(fitbit.token_url, client_secret=CLIENT_SECRET,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    fitbit = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    return fitbit.get('https://api.fitbit.com/1/user/-/profile.json')
    # jsonify(fitbit.get('https://api.fitbit.com/1/user/-/profile.json').json())


# @app.route("/callback")
# def access():
#    return "Success"


# @app.route('/login/fitbit-api')
# def login():
#    return redirect(url_for("fitbit-api.login"))


# Redirect URI = http://127.0.0.1:
if __name__ == '__main__':
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.run(host="http://127.0.0.1", port=5000, debug=True)

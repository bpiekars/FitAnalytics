# from fitbit import gather_keys_oauth2 as oauth2  # gather_keys_oauth2.py file needs to be in same directory as main file
from flask import Flask, redirect, url_for, render_template, jsonify
from flask_dance import OAuth2ConsumerBlueprint
import os
import datetime

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_ID = '#####'  # App's Client ID from Fitbit Dev portal
CLIENT_SECRET = '#######'  # App's Client Secret key from Fitbit Dev portal
scopes = ["activity",
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
# Flask OAuth2 Custom Blueprint for Fitbit API
app = Flask(__name__)
fitbit = OAuth2ConsumerBlueprint(
    "fitbit-api", __name__,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    base_url="https://www.fitbit.com",
    token_url="https://api.fitbit.com/oauth2/token",
    authorization_url="https://www.fitbit.com/oauth2/authorize",
    scope=scopes
)
app.register_blueprint(fitbit, url_prefix="/login")
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    # return redirect(url_for("fitbit-api.login"))
    return render_template('index.html')
    # return redirect(url_for("fitbit-api.login"))
    # fitbit = fitbit_blueprint.session_class
    # fitbit = OAuth2Session(CLIENT_ID)
    # State is used to prevent CSRF, keep this for later.\
    # authorization_url, state = fitbit.authorization_url(authorization_base_url)
    # state = fitbit_blueprint.state
    # return redirect(url_for("fitbit-api.login"))
    # return redirect(fitbit_blueprint.authorization_url)
    # return "Hello, world"


# Step 2: User authorization, this happens on the provider.

@app.route("/login/fitbit-api/authorized", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    # fitbit = OAuth2Session(CLIENT_ID, state=fitbit_blueprint.session)
    # token = fitbit.fetch_token(fitbit.token_url, client_secret=CLIENT_SECRET,
    #                          authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    # session['oauth_token'] = token
    return redirect(url_for('/profile'))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    # fitbit_session = OAuth2Session(CLIENT_ID, token=fitbit.token)
    # r = fitbit_session.get('https://api.fitbit.com/1/user/-/sleep/goal.json')
    # return fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')
    # '-' represents the currently logged in user
    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json').json())
    # return redirect(url_for(fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')))


# @app.route("/callback")
# def access():
#    return "Success"

@app.route("/daily")
def report():
    today = datetime.date.today()
    # '-' represents the currently logged in user
    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/activities/date/{}.json'.format(today)).json())


@app.route('/login/fitbit-api')
def login():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    if not fitbit.authorized:
        return redirect(fitbit.base_url)
    fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')

    # fitbit = fitbit_blueprint.session_class

    # fitbit = OAuth2Session(CLIENT_ID)
    # State is used to prevent CSRF, keep this for later.\
    # authorization_url, state = fitbit.authorization_url(authorization_base_url)
    # state = fitbit_blueprint.state
    # return redirect(url_for("fitbit-api.login"))
    # return redirect(fitbit_blueprint.authorization_url)


# Redirect URI = http://127.0.0.1:
if __name__ == '__main__':
    # This allows us to use a plain HTTP callback
    app.run(host="http://127.0.0.1", port=5000, debug=True)
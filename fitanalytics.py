import os
import datetime
from flask import Flask, redirect, url_for, render_template, jsonify
from flask_dance import OAuth2ConsumerBlueprint
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import io
import base64

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
today = datetime.date.today()

#  Both Client ID and Client Secret key are stored in Windows Env Variables on my local machine
client_id = os.environ.get('CLIENT_ID')  # App's Client ID from Fitbit Dev portal
client_secret = os.environ.get('CLIENT_SECRET')  # App's Client Secret key from Fitbit Dev portal
# print(CLIENT_ID)
# print(CLIENT_SECRET)
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
    client_id=client_id,
    client_secret=client_secret,
    base_url="https://www.fitbit.com",
    token_url="https://api.fitbit.com/oauth2/token",
    authorization_url="https://www.fitbit.com/oauth2/authorize",
    scope=scopes
)
app.register_blueprint(fitbit, url_prefix="/login")
app.secret_key = os.urandom(24)  # App secret must be set to access Flask's session object


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


# @app.route("/profile", methods=['GET', 'POST'])
# def profile():
#    """Fetching a protected resource using an OAuth 2 token.
#    """
#    # fitbit_session = OAuth2Session(CLIENT_ID, token=fitbit.token)
#    # r = fitbit_session.get('https://api.fitbit.com/1/user/-/sleep/goal.json')
#    # return fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')
#    # '-' represents the currently logged in user
#    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json').json())
# return redirect(url_for(fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')))


# @app.route("/callback")
# def access():
#    return "Success"

@app.route("/daily")
def report():
    # '-' represents the currently logged in user
    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/activities/date/{}.json'.format(today)).json())


@app.route("/heart")
def hr():
    data = jsonify(fitbit.session.get(
        'https://api.fitbit.com/1/user/-/activities/heart/date/{}/today/{}.json'.format('2020-01-15', '1min')).json())
    return data


@app.route("/weight")
def weight():
    data = jsonify(fitbit.session.get(
        'https://api.fitbit.com/1/user/-/body/log/weight/date/{}.json'.format('2020-01-15')).json())
    return data


@app.route('/plot')
def build_plot():
    img = io.BytesIO()

    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


@app.route("/profile")
def profile():
    link = 'https://api.fitbit.com/1/user/-/profile.json'
    data = jsonify(fitbit.session.get(link)).json()
    return data
    # return json.dumps(data, indent=4, sort_keys=True)


@app.route('/login/fitbit-api')
def login():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    # if not fitbit.authorized:
    #    return redirect(fitbit.base_url)
    # fitbit.session.get('https://api.fitbit.com/1/user/-/profile.json')

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

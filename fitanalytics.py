import os
import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_dance import OAuth2ConsumerBlueprint

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # temporarily ignores https requirement for testing
today = datetime.date.today()

#  Both Client ID and Client Secret key are stored in Windows Env Variables on my local machine
client_id = os.environ.get('CLIENT_ID')  # App's Client ID from Fitbit Dev portal
client_secret = os.environ.get('CLIENT_SECRET')  # App's Client Secret key from Fitbit Dev portal
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


@app.route("/", methods=['GET', "POST"])
def index():
    return render_template('index.html')


@app.route("/daily", methods=['GET', 'POST'])
def report():
    # '-' represents the currently logged in user
    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/activities/date/{}.json'.format(today)).json())


@app.route("/heart", methods=['GET', 'POST'])
def hr():
    data = jsonify(fitbit.session.get(
        'https://api.fitbit.com/1/user/-/activities/heart/date/{}/today/{}.json'.format('2020-01-15', '1min')).json())
    return data


@app.route("/weight", methods=['GET', 'POST'])
def weight():
    link = 'https://api.fitbit.com/1/user/-/body/log/weight/date/{}.json'.format('2020-01-15')
    resp = fitbit.session.get(link)
    print(resp)
    resp.headers['Accept-Language'] = 'en-US'
    resp.headers['Accept-Locale'] = 'en-US'
    print(resp)
    return resp.json()


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    link = 'https://api.fitbit.com/1/user/-/profile.json'
    response = fitbit.session.get(link)
    data = response.json()
    # data = jsonify(fitbit.session.get(link).json())
    return "Welcome, {}! Thanks for authenticating.".format(data['user']['displayName'])


if __name__ == '__main__':
    # This allows us to use a plain HTTP callback
    app.run(host="http://127.0.0.1", port=5000, debug=True)

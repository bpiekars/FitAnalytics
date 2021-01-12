import os
import datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_dance import OAuth2ConsumerBlueprint
import matplotlib.pyplot as plt
import io
import base64

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
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


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/daily")
def report():
    # '-' represents the currently logged in user
    return jsonify(fitbit.session.get('https://api.fitbit.com/1/user/-/activities/date/{}.json'.format(today)).json())


@app.route("/heart", methods=["POST"])
def hr():
    # Validate the request body contains JSON
    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
        # Print the dictionary
        print(req)
        # Return a string along with an HTTP status code
        return "JSON received!", 200
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
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
    response = fitbit.session.get(link)
    #print(response.json())
    profile = response.json()
    print(profile['user']['displayName'])

    data = jsonify(fitbit.session.get(link).json())
    print(data.is_json)
    return "Welcome, {}! Thanks for authenticating.".format(profile['user']['displayName'])


# Redirect URI = http://127.0.0.1:
if __name__ == '__main__':
    # This allows us to use a plain HTTP callback
    app.run(host="http://127.0.0.1", port=5000, debug=True)

from flask import Flask, redirect, url_for, render_template
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_sqlalchemy import SQLAlchemy

# TODO : Work with OAuth2 Authorization Flow to Hide client_id, client_secret, access_token, refresh_token
# TODO : Get flask to redirect to fitbit authorization login page
# TODO : Get authorization/access tokens working

# ./gather_keys_oauth2.py
CLIENT_ID = '#####'  # OAuth 2.0 Client ID
CLIENT_SECRET = 'null'
access_token = 'null'  # When using Implicit Grant Flow, can change lifetime of the access token
refresh_token = 'null'  # Refreshing token requires use of client secret
#  Access tokens obtained via the Implicit Grant Flow only stored on the device used to obtain the authorization
# server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
# server.browser_authorize()
# ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
# REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
# auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
#                            refresh_token=REFRESH_TOKEN)
# auth2_client.sleep()

# Flask OAuth2 Custom Blueprint for Fitbit API
app = Flask(__name__)
# Configuring an app db using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # Initializing a SQLite database
# Need to create Database columns
fitbit_blueprint = OAuth2ConsumerBlueprint(
    "fitbit-api", __name__,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    base_url="https://www.fitbit.com",
    token_url="https://api.fitbit.com/oauth2/token",
    authorization_url="https://www.fitbit.com/oauth2/authorize",
)
app.register_blueprint(fitbit_blueprint, url_prefix="/login")

app.secret_key = CLIENT_SECRET  # Replace this


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/success")
def access():
    return redirect(url_for("https://api.fitbit.com/1/user/-/profile.json"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for("fitbit-api.login"))


# Redirect URI = http://127.0.0.1:
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

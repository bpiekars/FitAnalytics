import fitbit
from flask import Flask, redirect, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint

# TODO : Work with OAuth2 Authorization Flow to Hide client_id, client_secret, access_token, refresh_token
# TODO : Get flask to redirect to fitbit authorization login page
# TODO : Get authorization/access tokens working

# ./gather_keys_oauth2.py
CLIENT_ID = 'secret'  # OAuth 2.0 Client ID
CLIENT_SECRET = 'secret'  # Client Secret
access_token = "null"  # When using Implicit Grant Flow, can change lifetime of the access token
refresh_token = "null"  # Refreshing token requires use of client secret
#  Access tokens obtained via the Implicit Grant Flow only stored on the device used to obtain the authorization
#  If your application has a web server component, application should use the Authorization Code Grant Flow
authd_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                             access_token='secret',
                             refresh_token='secret')
authd_client.sleep()

# Flask OAuth2 Custom Blueprint for Fitbit API
app = Flask(__name__)
fitbit_blueprint = OAuth2ConsumerBlueprint(
    "Fitbit Web API", __name__,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    base_url="www.fitbit.com",
    token_url="https://api.fitbit.com/oauth2/token",
    authorization_url="https://www.fitbit.com/oauth2/authorize",
)
app.register_blueprint(fitbit_blueprint, url_prefix="/login")


# app.secret_key = CLIENT_SECRET  # Replace this

@app.route("/")
def index():
    if not authd_client:
        return redirect(url_for("https://www.fitbit.com/oauth2/authorize"))
        resp = fitbit_blueprint.session.get("/user")
        assert resp.ok
        print("Here's the content of my response: " + resp.content)
    # return 'Hello world!'


# Redirect URI = http://127.0.0.1:8080/
if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)

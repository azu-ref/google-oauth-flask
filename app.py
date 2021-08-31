import os

from flask import Flask, url_for, session, redirect, Response
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret'

print(os.getenv("GOOGLE_CLIENT_ID"))
print(os.getenv("GOOGLE_CLIENT_SECRET"))

#aouth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth?hd=3mit.dev',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
)

@app.route("/")
def hello_world():
    email = dict(session).get('email', None)
    return f"<p>Hello, {email}</p>"

@app.route('/login')
def login():
    # google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    print(resp)
    profile = resp.json()
    email = profile['email']
    domain = email.split('@')[1]
    # if domain != '3mit.dev':
    #     return Response("{\"Error\":\"Unathorized\"}", status=401, mimetype='application/json')
    session['email'] = email
    # do something with the token and profile
    # return {"token": token}
    return redirect("https://www.google.com")
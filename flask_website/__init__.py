from flask import Flask, session, g, render_template
from flask_cors import CORS
from flask_environments import Environments


app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
# env = Environments(app)
# env.from_object('config')

# app.config.from_object('config')


from flask_website.views import public
from flask_website.views import app_url

app.register_blueprint(public.mod)
app.register_blueprint(app_url.mod)
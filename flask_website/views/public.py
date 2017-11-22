from flask import Blueprint, render_template, jsonify
mod = Blueprint('public', __name__, url_prefix='/public')
from flask_website.database import User

@mod.route('/')
def hello_world():
    print(User.query.filter_by(username='xiaotang').all()[0].username)
    return 'Hello World!'

@mod.route('/index')
def hello():
    return render_template('public/index.html',name='xiaotang');


    
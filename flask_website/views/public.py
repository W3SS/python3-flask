from flask import Blueprint, render_template, jsonify,request
mod = Blueprint('public', __name__, url_prefix='/public')
from flask_website.database import User,Indent,IndentProduct,Cart,Address,Article,Product,Comment,Classify
import time,hashlib,json

@mod.route('/')
def hello_world():
    print(User.query.filter_by(username='xiaotang').all()[0].username)
    return 'Hello World!'

@mod.route('/index')
def hello():
    return render_template('public/index.html',name='xiaotang')

@mod.route('/product/add',methods=['POST'])
def product_add():
    name = request.args.get('name')
    price = request.args.get('price')
    pid = request.args.get('pid')
    addTime = time.time()
    product = Product(name=name,price=price,pid=pid,add_time=addTime)
    Product.insert(product)
    return jsonify({'status': 1})

@mod.route('/product/edit',methods=['POST'])
def product_edit():
    id = request.args.get('id')
    name = request.args.get('name')
    price = request.args.get('price')
    pid = request.args.get('pid')
    addTime = time.time()

    product = Product(id=id,name=name,price=price,pid=pid,add_time=addTime)
    Product.edit(product)
    return jsonify({'status': 1})

@mod.route('/classify/add',methods=['POST'])
def classify_add():
    name = request.args.get('name')
    classify = Classify(name=name)
    Classify.insert(classify)
    return jsonify({'status': 1})

@mod.route('/article/add',methods=['POST'])
def article_add():
    title = request.args.get('title')
    content = request.args.get('content')
    userId = request.args.get('userId')
    article = Article(title=title,content=content,user_id=userId)
    Article.insert(article)
    return jsonify({'status': 1})

@mod.route('/user/add',methods=['POST'])
def user_add():
    m = hashlib.md5()
    phone = request.args.get('phone')
    username = request.args.get('username')
    password = request.args.get('password')
    addTime = time.time()
    roleId = request.args.get('roleId')
    m.update(password.encode("UTF-8"))
    psw = m.hexdigest()
    user = User(phone=phone,username=username,password=psw,role_id=roleId,add_time=addTime)
    User.insert(user)
    return jsonify({'status': 1})



    
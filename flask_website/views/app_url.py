from flask import Flask,Blueprint, render_template, request,jsonify,make_response
mod = Blueprint('app_url', __name__, url_prefix='/app')

from flask_website.database import User,Indent,IndentProduct,Cart,Address,Article,Product
import hashlib,json,time
app = Flask(__name__)

# from flask_website.utils.aliyun_sms import AliyunSMS
from functools import wraps


# def cors(func):
#     @wraps(func)
#     def wrapper_func(*args, **kwargs):
#         r = make_response(func(*args, **kwargs))
#         r.headers['Access-Control-Allow-Origin'] = '*'
#         r.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
#         allow_headers = "Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type"
#         r.headers['Access-Control-Allow-Headers'] = allow_headers
#         return r
#
#     return wrapper_func

@mod.route('/login',methods=['POST'])
def login():
    m = hashlib.md5()
    
    username = request.args.get('username')
    password = request.args.get('password')
    phone = request.args.get('phone')
    # password = password.encode('utf-8')

    m.update(password.encode("UTF-8"))
    psw = m.hexdigest()
    print(psw)

    name = User.query.filter_by(phone=phone,password=psw).first()

    if name is None:
        row = {
            'status': 0
        }
        return json.dumps(row)
    # dict1 = []
    # for x in name:
    # 	dict1.append(x.to_json())
    dict = name.to_json()
    x = time.localtime(dict['addTime'])  # localtime参数为float类型，这里1317091800.0为float类型
    addTime = time.strftime('%Y-%m-%d %H:%M:%S', x)
    dict['status'] = 1
    dict['add_time'] = addTime
    return json.dumps(dict)

@mod.route('/register',methods=['POST'])
def register():
    m = hashlib.md5()
    phone = request.args.get('phone')
    password = request.args.get('password')
    m.update(password.encode("UTF-8"))
    psw = m.hexdigest()
    now = int(time.time())
    me = User(phone=phone,password=psw,add_time=now)
    me.insert(me)
    dict = {'status': 1,'user': psw}
    return json.dumps(dict)

@mod.route('/indent',methods=['POST'])
def indent():
    userId = request.args.get('userId')
    indent = Indent.query.filter_by(user_id=userId).all()
    return jsonify(indent = [i.serialize() for i in indent])


@mod.route('/indent_detail',methods=['POST'])
def indent_detail():
    indentId = request.args.get('indentId')
    # indent = IndentProduct.query(Indent,IndentProduct).join(Indent, Indent.id == IndentProduct.indent_id).filter_by(id=indentId).all()

    return IndentProduct.getDetail(indentId)

# 获取购物车
@mod.route('/cart',methods=['POST'])
def cart():
    userId = request.args.get('userId')
    cart = Cart.query.filter_by(user_id=userId).all()
    return jsonify(indent=[i.serialize() for i in indent])

@mod.route('/get_in_cart',methods=['POST'])
def get_in_cart():
    userId = request.args.get('userId')
    product_id = request.args.get('productId')
    count = request.args.get('count')
    addTime = int(time.time())
    cart = Cart(user_id=userId,product_id=product_id,count=count,add_time=addTime)
    Cart.insert(cart)
    dict = {'status': 1}
    return jsonify(dict)


@mod.route('/address',methods=['POST'])
def address():
    userId = request.args.get('userId')
    return Address.getAddress(userId)

@mod.route('/address/add',methods=['POST'])
def add_address():
    userId = request.args.get('userId')
    province = request.args.get('province')
    city = request.args.get('city')
    county = request.args.get('county')
    street = request.args.get('street')
    phone = request.args.get('phone')
    username = request.args.get('username')
    addTime = int(time.time())
    address = Address(province=province,
                      city=city,
                      county=county,
                      street=street,
                      phone=phone,
                      username=username,
                      user_id=userId,
                      add_time=addTime)
    Address.insert(address)
    dict = {'status': 1}
    return jsonify(dict)

@mod.route('/address/edit',methods=['POST'])
def edit_address():
    address_id = request.args.get('addressId')
    province = request.args.get('province')
    city = request.args.get('city')
    county = request.args.get('county')
    street = request.args.get('street')
    phone = request.args.get('phone')
    username = request.args.get('username')
    addTime = int(time.time())
    address = Address(id=address_id,
                      province=province,
                      city=city,
                      county=county,
                      street=street,
                      phone=phone,
                      username=username,
                      add_time=addTime)
    result = Address.update(address)
    dict = {'status': result}
    return jsonify(dict)

@mod.route('/article',methods=['POST'])
def get_article():
    dict = Article.getArticle()
    return jsonify(articles=[i.serialize() for i in dict])

@mod.route('/get_product',methods=['POST'])
def get_product():
    pid = request.args.get('pid')
    dict = Product.getProductByPid(pid)
    return jsonify(products=[i.serialize() for i in dict])


@mod.route('/userinfo',methods=['POST'])
def userinfo():
    userId = request.args.get('userId')
    user = User.getUserinfo(userId)
    return jsonify(user.to_json())

@mod.route('/user/edit',methods=['POST'])
def user_edit():
    userId = request.args.get('userId')
    username = request.args.get('username')
    user = User(username=username,id=userId)
    User.update(user)
    return jsonify({'status':1})

@mod.route('/user/repassword',methods=['POST'])
def repassword():
    userId = request.args.get('userId')
    password = request.args.get('password')
    m = hashlib.md5()
    m.update(password.encode("UTF-8"))
    psw = m.hexdigest()
    user = User(password=psw, id=userId)
    User.update(user)
    return jsonify({'status': 1})



# @mod.route('/')

# @mod.route('/validation',methods=["POST"])
# def validation():
#     phone = request.args.get('phone')
#     count = User.query.filter_by(phone=phone).count()
#     print('hello world')
#     sms = AliyunSMS(app)
#     sms.send_single("18868748898", '富春江app', 'SMS_5250008', {"code": 234232})
#     # sms.send_single("18868748898", app.config["ALISMS_SIGN"], app.config["ALISMS_TPL_REGISTER"], {"code": 234232})
#     if(count>0):
#         row = {
#             'status': 0
#         }
#         return json.dumps(row)
#
#     row = {
#         'status': 1,
#         'code': '123456',
#     }
#     return json.dumps(row)
#     return str(count)





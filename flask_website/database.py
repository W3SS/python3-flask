from flask.ext.sqlalchemy import SQLAlchemy
from flask_website import app
from flask import jsonify
from sqlalchemy.orm import sessionmaker
import json
# engine = create_engine('sqlite:///:memory:', echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()

# 服务器
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root1:123456@127.0.0.1:3306/fuchunjiang'
# 本地环境
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/fuchunjiang'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)
import json


class User(db.Model):
    # 定义表名
    __tablename__ = 'x_user'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    add_time = db.Column(db.Integer)

    def __init__(self, phone=None,password=None,username=None,add_time=None):
        self.password = password
        self.phone = phone
        self.username = username
        self.add_time = add_time

    # def __repr__(self):
    #     return '{username:'+self.username+'}'

    def insert(self,user):
        db.session.add(user)
        db.session.commit()


    # repr()方法显示一个可读字符串，虽然不是完全必要，不过用于调试和测试还是很不错的。

    def to_json(self):
        return {
            'username': self.username,
            'phone': self.phone,
            'addTime': self.add_time
        }

# 订单类
class Indent(db.Model):

    # 表名
    __tablename__ = 'x_indent'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    number = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    price = db.Column(db.String(255))
    address = db.Column(db.String(255))
    add_time = db.Column(db.Integer)

    def __init__(self, number=None,user_id=None,price=None,address=None,add_time=None):
        self.number = number
        self.user_id = user_id
        self.price = price
        self.address = address
        self.add_time = add_time

    def __repr__(self):
        dict = {
            'number': self.number,
            'user_id': self.user_id,
            'price': self.price,
            'address': self.address,
            'add_time': self.add_time,
        }

        return json.dumps(dict)

    def insert(self, indent):
        db.session.add(indent)
        db.session.commit()

    def serialize(self):
        return {
            'number': self.number,
            'user_id': self.user_id,
            'price': self.price,
            'address': self.address,
            'add_time': self.add_time,
        }

# 订单详情类
class IndentProduct(db.Model):

    # 表名
    __tablename__ = 'x_indent_product'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    indent_id = db.Column("indent_id", db.Integer, db.ForeignKey("Indent.id"))
    price = db.Column(db.String(255))
    count = db.Column(db.String(255))

    def __init__(self, product_id=None,indent_id=None,price=None,count=None):
        self.product_id = product_id
        self.indent_id = indent_id
        self.price = price
        self.count = count

    def __repr__(self):
        dict = {
            'product_id': self.product_id,
            'indent_id': self.indent_id,
            'price': self.price,
            'count': self.count,
        }
        return json.dumps(dict)

    def insert(self, indentDetail):
        db.session.add(indentDetail)
        db.session.commit()

    @staticmethod
    def getDetail(indentId):
        data = db.session.query(IndentProduct).\
            join(Indent, Indent.id == IndentProduct.indent_id).\
            filter(IndentProduct.indent_id==indentId).\
            with_entities(IndentProduct.price,IndentProduct.product_id,Indent.address,Indent.add_time).\
            all()
        # data = db.session.query(IndentProduct.price, IndentProduct.product_id, Indent.address).join(Indent).filter(
        #     IndentProduct.indent_id == indentId).all()
        # data = db.session.execute('select * from x_indent_product as IndentProduct where IndentProduct.indent_id = '+indentId).first()
        # data = db.session.query(IndentProduct).filter(IndentProduct.indent_id==indentId).all()
        print(data)
        list = [dict(zip(result.keys(), result)) for result in data]

        print(type(list))
        return jsonify(list)


    def serialize(self):
        return {
            'product_id': self.product_id,
            'indent_id': self.indent_id,
            'price': self.price,
            'count': self.count,
        }

    def serialize2(self):
        return {
            'product_id': self.product_id,
            'indent_id': self.indent_id,
            'price': self.price,
            'count': self.count,

        }

# 购物车列表
class Cart(db.Model):

    # 表名
    __tablename__ = 'x_cart'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    count = db.Column(db.Integer)
    add_time = db.Column(db.Integer)


    def __init__(self, product_id=None,user_id=None,count=None,add_time=None):
        self.product_id = product_id
        self.user_id = user_id
        self.count = count
        self.add_time = add_time

    def __repr__(self):
        dict = {
            'product_id': self.product_id,
            'user_id': self.user_id,
            'count': self.count,
            'add_time': self.add_time,
        }
        return json.dumps(dict)

    def insert(self, cart):
        db.session.add(cart)
        db.session.commit()

    def serialize(self):
        return {
            'product_id': self.product_id,
            'user_id': self.user_id,
            'count': self.count,
            'add_time': self.add_time,
        }

# 收货地址表
class Address(db.Model):

    # 表名
    __tablename__ = 'x_address'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    province = db.Column(db.String(20))
    city = db.Column(db.String(20))
    county = db.Column(db.String(30))
    street = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(255))
    add_time = db.Column(db.Integer)


    def __init__(self, province=None,city=None,county=None,street=None,phone=None,username=None,add_time=None):
        self.province = province
        self.city = city
        self.county = county
        self.street = street
        self.phone = phone
        self.username = username
        self.add_time = add_time

    def __repr__(self):
        dict = {
            'province': self.province,
            'city': self.city,
            'county': self.county,
            'street': self.street,
            'phone': self.phone,
            'username': self.username,
            'add_time': self.add_time,
        }
        return json.dumps(dict)

    def insert(self, address):
        db.session.add(address)
        db.session.commit()

    def serialize(self):
        return {
            'province': self.province,
            'city': self.city,
            'county': self.county,
            'street': self.street,
            'phone': self.phone,
            'username': self.username,
            'add_time': self.add_time,
        }

# 文章类
class Article(db.Model):

    # 表名
    __tablename__ = 'x_article'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer)
    file_id = db.Column(db.Integer)


    def __init__(self, title=None,content=None,user_id=None,file_id=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.file_id = file_id

    def __repr__(self):
        dict = {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'file_id': self.file_id,
        }
        return json.dumps(dict)

    def insert(self, article):
        db.session.add(article)
        db.session.commit()

    def serialize(self):
        return {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'file_id': self.file_id,
        }

# 菜单类表
class Classify(db.Model):

    # 表名
    __tablename__ = 'x_classify'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        dict = {
            'name': self.name,
        }
        return json.dumps(dict)

    def insert(self, classify):
        db.session.add(classify)
        db.session.commit()

    def serialize(self):
        return {
            'name': self.name,
        }

# 评论表
class Comment(db.Model):

    # 表名
    __tablename__ = 'x_comment'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer)


    def __init__(self, title=None,content=None,user_id=None):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        dict = {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
        }
        return json.dumps(dict)

    def insert(self, comment):
        db.session.add(comment)
        db.session.commit()

    def serialize(self):
        return {
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
        }

# 文件表
class File(db.Model):

    # 表名
    __tablename__ = 'x_file'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    add_time = db.Column(db.Integer)


    def __init__(self, file_name=None,file_path=None,add_time=None):
        self.file_name = file_name
        self.file_path = file_path
        self.add_time = add_time

    def __repr__(self):
        dict = {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'add_time': self.add_time,
        }
        return json.dumps(dict)

    def insert(self, file):
        db.session.add(file)
        db.session.commit()

    def serialize(self):
        return {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'add_time': self.add_time,
        }

# 产品类
class Product(db.Model):

    # 表名
    __tablename__ = 'x_product'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(255))
    add_time = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    file_id = db.Column(db.Integer)


    def __init__(self, name=None,price=None,add_time=None,pid=None,file_id=None):
        self.name = name
        self.price = price
        self.add_time = add_time
        self.pid = pid
        self.file_id = file_id

    def __repr__(self):
        dict = {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'add_time': self.add_time,
            'pid': self.pid,
            'file_id': self.file_id,
        }
        return json.dumps(dict)

    def insert(self, product):
        db.session.add(product)
        db.session.commit()

    def serialize(self):
        return {
            'file_name': self.file_name,
            'file_path': self.file_path,
            'add_time': self.add_time,
            'pid': self.pid,
            'file_id': self.file_id,
        }

# 心愿类
class WishList(db.Model):

    # 表名
    __tablename__ = 'x_wish_list'

    # 列对象
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    add_time = db.Column(db.Integer)


    def __init__(self, product_id=None,user_id=None,add_time=None):
        self.product_id = product_id
        self.user_id = user_id
        self.add_time = add_time

    def __repr__(self):
        dict = {
            'product_id': self.product_id,
            'user_id': self.user_id,
            'add_time': self.add_time,
        }
        return json.dumps(dict)

    def insert(self, wishList):
        db.session.add(wishList)
        db.session.commit()

    def serialize(self):
        return {
            'product_id': self.product_id,
            'user_id': self.user_id,
            'add_time': self.add_time,
        }

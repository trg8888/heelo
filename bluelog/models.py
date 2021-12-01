from datetime import datetime
from bluelog.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Auto(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    remarks = db.Column(db.String(300))
    exegesis = db.Column(db.String(30))
    least = db.Column(db.Float())
    maximum = db.Column(db.Float())
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    subcategorys = db.relationship('Subcategory',back_populates='major',cascade='all, delete')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15),)
    exegesis = db.Column(db.String(30))
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    disable = db.Column(db.Boolean, index=True, default=False)
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    major = db.relationship('Major', back_populates='subcategorys')
    picture = db.relationship('Picture',back_populates='subcategorys',cascade='all, delete')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    description = db.Column(db.Text) # 描述
    attribute = db.Column(db.String(150)) # 属性
    color = db.Column(db.String(150)) # 颜色
    picture = db.Column(db.String(150)) # 图片
    price = db.Column(db.Float(5,2)) # 价格
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    subcategorys_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    subcategorys = db.relationship('Subcategory',back_populates='picture')

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class PrivacySecurity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class PaymentMethods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class ReturnPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Subcategory_(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class basicsettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), index=True)
    Keyword = db.Column(db.String(150), index=True)
    description = db.Column(db.String(500), index=True)
    frequency = db.Column(db.Integer, index=True, default=0)  # 次数
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

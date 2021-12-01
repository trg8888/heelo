from flask import Blueprint,render_template,request,json,redirect,url_for,flash,jsonify
from bluelog.extensions import db
from bluelog.models import Auto
from flask_login import login_user, current_user
from bluelog.utils import validate_token, generate_token
from bluelog.settings import Operations
from bluelog.forms import LoginForm, Landed
from bluelog.email import send_confirm_email
from sqlalchemy import or_, and_

auto_bp = Blueprint('auto', __name__)


@auto_bp.route('/',methods=['GET','POST'])
def auto_login():
    if current_user.is_authenticated:
        return redirect(url_for('auto_manage.auto_manage_login'))
    form = Landed()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Auto.query.filter(and_(Auto.username==username,Auto.confirmed==True)).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user)
                return json.dumps({'code':'200'})
            else:
                return json.dumps({'code':'201'})
        else:
            return json.dumps({'code':'201'})
    return render_template('auto/index.html',form=form)

@auto_bp.route('/application',methods=['GET','POST'])
def application():
    if current_user.is_authenticated:
        return redirect(url_for('auto_manage.auto_manage_login'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        phone = form.phone.data
        email = form.email.data
        data = Auto.query.filter(or_(Auto.username == username, Auto.phone == phone, Auto.email== email)).all()
        if data:
            flash('账号或手机号码或邮箱已存在')
            return render_template('auto/application.html',form=form)
        auto = Auto(username=username,phone=phone,email=email)
        auto.set_password(password=password)
        token = generate_token(email=email,operation='confirm',expire_in=3600)
        token = str(token, 'utf-8')
        send_confirm_email(subject='注册验证',email=email, token=token, username=username)
        db.session.add(auto)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash('存在异常 联系管理员')
            return render_template('auto/application.html',form=form)
        flash('注册成功请在邮箱中激活账户')
        return render_template('auto/application.html',form=form)

    return render_template('auto/application.html',form=form)

@auto_bp.route('/confirm/<token>')
def confirm(token):
    if validate_token(token=token, operation=Operations.CONFIRM):
        flash('账号已确定.', 'success')
        return redirect(url_for('auto.auto_login'))
    else:
        flash('连接已失效.', 'danger')
        return redirect(url_for('auto.auto_login'))

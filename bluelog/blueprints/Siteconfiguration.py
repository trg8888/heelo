import json

from flask import Blueprint,render_template,request,current_app
from bluelog.extensions import db
from flask_login import login_required
from bluelog.forms import About
from bluelog.models import About as About_sql, PrivacySecurity as PrivacySecurity_sql
from bluelog.models import PaymentMethods as PaymentMethods_sql
from bluelog.models import Subcategory_ as Subcategory_sql, Faq as Faq_sql
from bluelog.models import basicsettings as basicsettings_sql
from bluelog.forms import basicsettings as basicsettings_forms
from flask_login import current_user

configuration_bp = Blueprint('configuration', __name__)


@configuration_bp.route('/About_Us', methods=['GET'])
@login_required
def About_Us():
    form = About()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =About_sql.query.filter_by(auto_id=current_user.id).order_by(About_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/About_Us.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/About_Us/management', methods=['POST'])
@login_required
def About_Us_management():
    name = request.form.get('name')
    if not name:
        return json.dumps({'code':405})
    about_sql =About_sql(name=name, auto_id = current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/About_Us/delete', methods=['POST'])
@login_required
def About_Us_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = About_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@configuration_bp.route('/About_Us/edit', methods=['POST'])
@login_required
def About_Us_edit():
    name = request.form.get('name')
    id = request.form.get('id')
    if not all([name,id]):
        return json.dumps({'code':405})
    about_sql = About_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.name = name
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})
@configuration_bp.route('/Privacy_Security', methods=['GET'])
@login_required
def Privacy_Security():
    form = About()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =PrivacySecurity_sql.query.filter_by(auto_id=current_user.id).order_by(PrivacySecurity_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/Privacy_Security.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/Privacy_Security/management', methods=['POST'])
@login_required
def Privacy_Security_management():
    name = request.form.get('name')
    if not name:
        return json.dumps({'code':405})
    about_sql =PrivacySecurity_sql(name=name, auto_id= current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception as ff:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/Privacy_Security/delete', methods=['POST'])
@login_required
def Privacy_Security_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = PrivacySecurity_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})


@configuration_bp.route('/Privacy_Security/edit', methods=['POST'])
@login_required
def Privacy_Security_edit():
    name = request.form.get('name')
    id = request.form.get('id')
    if not all([name,id]):
        return json.dumps({'code':405})
    about_sql = PrivacySecurity_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.name = name
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@configuration_bp.route('/Payment_Methods', methods=['GET'])
@login_required
def Payment_Methods():
    form = About()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =PaymentMethods_sql.query.filter_by(auto_id=current_user.id).order_by(PaymentMethods_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/Payment_Methods.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/Payment_Methods/management', methods=['POST'])
@login_required
def Payment_Methods_management():
    name = request.form.get('name')
    if not name:
        return json.dumps({'code':405})
    about_sql =PaymentMethods_sql(name=name, auto_id=current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception as ff:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/Payment_Methods/delete', methods=['POST'])
@login_required
def Payment_Methods_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = PaymentMethods_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})


@configuration_bp.route('/Payment_Methods/edit', methods=['POST'])
@login_required
def Payment_Methods_edit():
    name = request.form.get('name')
    id = request.form.get('id')
    if not all([name,id]):
        return json.dumps({'code':405})
    about_sql = PaymentMethods_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.name = name
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@configuration_bp.route('/Subcategory', methods=['GET'])
@login_required
def Subcategory():
    form = About()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Subcategory_sql.query.filter_by(auto_id=current_user.id).order_by(Subcategory_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/Subcategory.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/Subcategory/management', methods=['POST'])
@login_required
def Subcategory_management():
    name = request.form.get('name')
    if not name:
        return json.dumps({'code':405})
    about_sql =Subcategory_sql(name=name, auto_id = current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception as ff:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/Subcategory/delete', methods=['POST'])
@login_required
def Subcategory_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = Subcategory_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})


@configuration_bp.route('/Subcategory/edit', methods=['POST'])
@login_required
def Subcategory_edit():
    name = request.form.get('name')
    id = request.form.get('id')
    if not all([name,id]):
        return json.dumps({'code':405})
    about_sql = Subcategory_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.name = name
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@configuration_bp.route('/Faq', methods=['GET'])
@login_required
def Faq():
    form = About()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Faq_sql.query.filter_by(auto_id=current_user.id).order_by(Faq_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/Faq.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/Faq/management', methods=['POST'])
@login_required
def Faq_management():
    name = request.form.get('name')
    if not name:
        return json.dumps({'code':405})
    about_sql =Faq_sql(name=name, auto_id = current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception as ff:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/Faq/delete', methods=['POST'])
@login_required
def Faq_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = Faq_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})


@configuration_bp.route('/Faq/edit', methods=['POST'])
@login_required
def Faq_edit():
    name = request.form.get('name')
    id = request.form.get('id')
    if not all([name,id]):
        return json.dumps({'code':405})
    about_sql = Faq_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.name = name
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@configuration_bp.route('/basicsettings', methods=['GET'])
@login_required
def basicsettings():
    form = basicsettings_forms()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =basicsettings_sql.query.filter_by(auto_id=current_user.id).order_by(basicsettings_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('configuration/basicsettings.html',form = form,datas=gets,pagination=pagination)

@configuration_bp.route('/basicsettings/management', methods=['POST'])
@login_required
def basicsettings_management():
    title = request.form.get('title')
    Keyword = request.form.get('Keyword')
    description = request.form.get('description')
    if not all([title,Keyword,description]):
        return json.dumps({'code':405})
    about_sql =basicsettings_sql(title=title,Keyword=Keyword,description=description, auto_id = current_user.id)
    db.session.add(about_sql)
    try:
        db.session.commit()
    except Exception as ff:
        db.session.rollback()
        return json.dumps({'code': 666})
    return json.dumps({'code': 200})

@configuration_bp.route('/basicsettings/delete', methods=['POST'])
@login_required
def basicsettings_delete():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code':405})
    about_sql = basicsettings_sql.query.get(int(user_id))
    if not about_sql:
        return json.dumps({'code':666})
    db.session.delete(about_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})


@configuration_bp.route('/basicsettings/edit', methods=['POST'])
@login_required
def basicsettings_edit():
    description = request.form.get('description')
    Keyword = request.form.get('Keyword')
    title = request.form.get('title')
    id = request.form.get('id')
    if not all([title,id,Keyword,description]):
        return json.dumps({'code':405})
    about_sql = basicsettings_sql.query.get(int(id))
    if not about_sql:
        return json.dumps({'code':666})
    about_sql.description = description
    about_sql.Keyword = Keyword
    about_sql.title = title
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})
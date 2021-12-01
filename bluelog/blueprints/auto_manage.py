from flask import Blueprint, render_template, json, request, current_app
from flask_login import login_required
from bluelog.forms import Major, Subcategory
from bluelog.models import Major as Major_sql
from bluelog.models import Subcategory as Subcategory_sql
from bluelog.models import Picture as Picture_sql
from bluelog.extensions import db
from flask_login import current_user

auto_manage_bp = Blueprint('auto_manage',__name__)

@auto_manage_bp.route('/')  #登陆首页
@login_required
def auto_manage_login():
    major_sql = Major_sql.query.filter_by(auto_id=current_user.id).count()
    subcategory_sql = Subcategory_sql.query.filter_by(auto_id=current_user.id).count()
    picture_sql = Picture_sql.query.filter_by(auto_id=current_user.id).count()

    return render_template('auto_manage/index.html',major_sql=major_sql,subcategory_sql=subcategory_sql,picture_sql=picture_sql)

@auto_manage_bp.route('/major_category')
@login_required
def major_category():
    form = Major()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Major_sql.query.filter_by(auto_id=current_user.id).order_by(Major_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('auto_manage/major_category.html',form = form,datas=gets,pagination=pagination)

@auto_manage_bp.route('/subcategory')
@login_required
def subcategory():
    form = Subcategory()
    major_data = Major_sql.query.filter_by(auto_id=current_user.id).all()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Subcategory_sql.query.filter_by(auto_id=current_user.id).order_by(Subcategory_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('auto_manage/subcategory.html', form=form, datas=gets, major_data= major_data, pagination= pagination)

@auto_manage_bp.route('/picture_management')
@login_required
def picture_management():
    form = Subcategory()
    major_data = Subcategory_sql.query.filter_by(auto_id=current_user.id).filter_by(disable=False).all()
    page = request.args.get('page',1,type=int)
    sort = request.args.get('sort',type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    if sort:
        pagination =Picture_sql.query.filter_by(auto_id=current_user.id).filter_by(subcategorys_id=int(sort)).join(Picture_sql.subcategorys).filter_by(disable=False).order_by(Picture_sql.timestamp.desc()).paginate(page,per_page=per_page)
    else:
        pagination =Picture_sql.query.filter_by(auto_id=current_user.id).join(Picture_sql.subcategorys).filter_by(disable=False).order_by(Picture_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('auto_manage/picture_management.html', form=form, datas=gets, major_data=major_data,pagination=pagination)

@auto_manage_bp.route('picture_management/get', methods=['POST'])
def picture_management_get():
    form = Subcategory()
    name = request.form.get('name')
    if not name:
        return '403',403
    major_data = Subcategory_sql.query.filter_by(auto_id=current_user.id).all()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Picture_sql.query.filter_by(auto_id=current_user.id).filter_by(name=name).order_by(Picture_sql.timestamp.desc()).paginate(page,per_page=per_page)
    gets = pagination.items
    return render_template('auto_manage/picture_management.html', form=form, datas=gets, major_data=major_data,pagination=pagination)






@auto_manage_bp.route('/major_category/management', methods=['POST'])
@login_required
def major_category_management():
    form = Major()
    name = form.name.data
    exegesis = form.exegesis.data
    remarks = form.remarks.data
    maximum = form.maximum.data
    least = form.least.data
    print(name,least,maximum)
    if not all([name,least,maximum]):
        return json.dumps({'code': '404', 'error': '缺少参数'})
    try:
        least = float(least)
        maximum = float(maximum)
    except ValueError:
        return json.dumps({'code': '404','error':'非法金额'})

    if least >= maximum:
        return json.dumps({'code': '404','error':'金额不能大于或者最大金额'})
    try:
        major_sql = Major_sql(name=name, exegesis=exegesis, least=least, maximum=maximum, remarks=remarks, auto_id=current_user.id)
        db.session.add(major_sql)
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404','error':'系统错误'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/major_category/edit', methods=['POST'])
@login_required
def major_category_edit():
    id = request.form.get('id')
    name = request.form.get('name')
    exegesis = request.form.get('exegesis')
    least = request.form.get('least')
    maximum = request.form.get('maximum')
    remarks = request.form.get('remarks')
    if not all([id,name,least,maximum]):
        return json.dumps({'code':404,'error':'缺少参数'})
    try:
        least = float(least)
        maximum = float(maximum)
    except ValueError:
        return json.dumps({'code': '404','error':'非法金额'})
    if least >= maximum:
        return json.dumps({'code': '404','error':'金额不能大于或者最大金额'})
    major_sql = Major_sql.query.get(int(id))
    if not major_sql:
        return json.dumps({'code':666,'error':'id错误，联系管理员'})
    major_sql.name = name
    major_sql.exegesis = exegesis
    major_sql.least = least
    major_sql.maximum = maximum
    major_sql.remarks = remarks
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404','error':'系统错误'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/major_category/delete', methods=['POST'])
@login_required
def major_category_delete():
    id = request.form.get('user_id')
    if not id:
        return json.dumps({'code':404})
    major_sql = Major_sql.query.get(int(id))
    if not major_sql:
        return json.dumps({'code':666})
    db.session.delete(major_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/subcategory/management', methods=['POST'])
@login_required
def subcategory_management():
    form = Subcategory()
    name = form.name.data
    exegesis = form.exegesis.data
    major_id = int(form.major_id.data)
    major_sql = Subcategory_sql(name=name,exegesis=exegesis,major_id =major_id, auto_id=current_user.id )
    db.session.add(major_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/subcategory/edit', methods=['POST'])
@login_required
def subcategory_edit():
    id = request.form.get('id')
    name = request.form.get('name')
    exegesis = request.form.get('exegesis')
    major_id = request.form.get('major_id')
    if not all([id,name,exegesis,major_id]):
        return json.dumps({'code':405})
    subcategory_sql = Subcategory_sql.query.get(int(id))
    if not subcategory_sql:
        return json.dumps({'code':666})
    subcategory_sql.name = name
    subcategory_sql.exegesis = exegesis
    subcategory_sql.major_id = major_id
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/subcategory/delete', methods=['POST'])
@login_required
def subcategory_delete():
    id = request.form.get('user_id')
    if not id:
        return json.dumps({'code':404})
    subcategory_sql = Subcategory_sql.query.get(int(id))
    if not subcategory_sql:
        return json.dumps({'code':666})
    db.session.delete(subcategory_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/picture_management/edit', methods=['POST'])
@login_required
def picture_management_edit():
    id = request.form.get('id')
    name = request.form.get('name')
    price = request.form.get('price')
    attribute = request.form.get('attribute')
    picture = request.form.get('picture')
    color = request.form.get('color')
    description = request.form.get('description')
    subcategory_id = request.form.get('subcategory_id')
    if not all([id,name,price,picture,description,subcategory_id]):
        return json.dumps({'code': 405})
    picture_sql =Picture_sql.query.get(id)
    if not picture_sql:
        return json.dumps({'code': 666})
    picture_sql.name = name
    picture_sql.price = price
    picture_sql.attribute = attribute
    picture_sql.picture = picture
    picture_sql.color = color
    picture_sql.description = description
    picture_sql.subcategory__id = subcategory_id
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/picture_management/delete', methods=['POST'])
@login_required
def picture_management_delete():
    id = request.form.get('user_id')
    if not id:
        return json.dumps({'code':404})
    picture_sql = Picture_sql.query.get(int(id))
    if not picture_sql:
        return json.dumps({'code':666})
    db.session.delete(picture_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code':'404'})
    return json.dumps({'code':'200'})

@auto_manage_bp.route('/all_delete',methods=['POST'])
@login_required
def all_delete():
    check_var = request.form.getlist("check_var[]")
    if not check_var:
        return json.dumps({'code':404})
    for _ in check_var:
        picture_sql = Picture_sql.query.get(int(_))
        if not picture_sql:
            return json.dumps({'code': 666})
        db.session.delete(picture_sql)
    try:
        db.session.commit()
    except Exception as zz:
        db.session.rollback()
        return json.dumps({'code': '404'})
    return json.dumps({'code': '200'})

@auto_manage_bp.route('/subcategory/disable', methods=['POST'])
@login_required
def disable():
    user_id = request.form.get('user_id')
    if not user_id:
        return json.dumps({'code': 404})
    subcategory_sql = Subcategory_sql.query.get(int(user_id))
    if not subcategory_sql:
        return json.dumps({'code': 666})
    if subcategory_sql.disable:
        subcategory_sql.disable = False
        try:
            db.session.commit()
        except Exception as zz:
            db.session.rollback()
            return json.dumps({'code': '404'})
        return json.dumps({'code': '300'})
    else:
        subcategory_sql.disable = True
        try:
            db.session.commit()
        except Exception as zz:
            db.session.rollback()
            return json.dumps({'code': '404'})
        return json.dumps({'code': '200'})
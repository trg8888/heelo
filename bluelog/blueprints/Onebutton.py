from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required
from bluelog.forms import About
import re
from bluelog.Backstage.Backstage import Configure
from bluelog.models import Major as Major_sql
from bluelog.models import Subcategory as Subcategory_sql
from bluelog.extensions import r
from bluelog.tasks import deity
from flask_login import current_user

onebutton_bp = Blueprint('onebutton', __name__)


@onebutton_bp.route('/')
@login_required
def index():
    form = About()
    data = Major_sql.query.filter_by(auto_id=current_user.id).all()
    redis_ = r.smembers('url')
    sku_list = r.lrange('sku','0','-1')
    data_list = []
    for sku in sku_list:
        task = deity.AsyncResult(sku)
        print(task.info)
        if task.state == 'SUCCESS':
            r.lrem('sku','0',sku)
        elif task.state == 'PROGRESS':
            data_list.append({'current': task.info.get('state', 0), 'url': task.info.get('url', 1)})
        else:
            data_list.append({'current': '系统错误', 'url': '系统错误'})
    return render_template("onebutton/index.html",form=form,data=data,redis_=redis_,data_list=data_list)


@onebutton_bp.route('/img', methods=['POST'])
@login_required
def img():
    if not r.smembers('img') and not r.smembers('url'):
        return jsonify({'code': '404'})
    r.delete('img')
    r.delete('url')
    return jsonify({'code': '200'})

@onebutton_bp.route('/get', methods=['POST'])
@login_required
def get_():
    datas = request.json
    data = datas.get('data')
    name = datas.get('name')
    pwd = datas.get('pwd')
    list_ = datas.get('list_')
    data_zd = datas.get('data_zd')
    if not all([data,name,pwd,list_]):
        return jsonify({'code': '404','error':'缺少参数'})
    list_ = list(set(list_))
    for _ in list_:
        __ = re.findall('.*?/grzh.*?-titan',_)
        if not __:
            return jsonify({'code': '404','error':'缺少配置网站'})
    ce = []
    for _ in data:
        if _.get('id') in ce:
            return jsonify({'code': '404','error':'大类有重复'})
        else:
            ce.append(_.get('id'))
        try:
            if int(_.get('int_id')) > Subcategory_sql.query.filter_by(major_id=int(_.get('id'))).count():
                return jsonify({'code': '404', 'error': '不能大于小类数量'})
        except ValueError:
            return jsonify({'code': '404', 'error': '您输入的指定类存在非法字符'})
    if data_zd:
        for _ in data_zd:
            if _.get('id') in ce:
                return jsonify({'code': '404', 'error': '指定大类有重复'})
            else:
                ce.append(_.get('id'))
            zz = _.get('zhiding').split(',')
            for i in zz:
                try:
                    float(i)
                    if int(_.get('int_id')) > Subcategory_sql.query.filter_by(major_id=int(_.get('id'))).count():
                        return jsonify({'code': '404', 'error': '不能大于小类数量'})
                except ValueError:
                    return jsonify({'code': '404', 'error': '您输入的指定类存在非法字符'})
    for url in list_:
        res = deity.delay(url=url,name=name,pwd=pwd,data=data,data_zd=data_zd)
        r.lpush('sku',res.id)

    return jsonify({'code': '404', 'error': '提交成功'})
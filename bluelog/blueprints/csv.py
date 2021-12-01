from flask import Blueprint, render_template, request
import uuid
from bluelog.email import updata_csv
csv_bp = Blueprint('csv',__name__)
from flask_login import current_user
from bluelog.extensions import r
from bluelog.email import data_updata_csv

@csv_bp.route('/')
def index():
    return render_template("csv/index.html")


@csv_bp.route('/post', methods=['POST'])
def post():
    name = uuid.uuid4().hex
    f = request.files.get('file')
    if f.filename.split('.')[-1] != 'csv':
        return '不支持csv以外的格式',400
    f.save('csv_/%s.csv' % name)
    updata_csv(name=name, user_id = current_user.id)
    return '200'

@csv_bp.route('/ruzhi')
def ruzhi():
    i = r.lrange('error','0','-1')
    data = []
    for _ in i:
        data.append(data_updata_csv(data_id=_))
    print(data)
    return render_template("csv/ruzhi.html",data=data)
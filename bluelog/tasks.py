from celery import Celery
from flask import current_app, render_template
from flask_mail import Message
from bluelog.extensions import mail
from bluelog.Backstage.Backstage import Configure
from urllib3.exceptions import SSLError
import csv
from bluelog.extensions import db
from bluelog.models import Subcategory, Picture
import time

celery_app = Celery(__name__)

@celery_app.task
def add(x, y):
    """
    加法
    :param x:
    :param y:
    :return:
    """
    return str(x + y)


@celery_app.task
def flask_app_context():
    """
    celery使用Flask上下文
    :return:
    """
    with current_app.app_context():
        return str(current_app.config)


@celery_app.task
def email_(template,subject,to,**kwargs):
    message = Message(current_app.config['ALBUMY_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    with current_app.app_context():
        mail.send(message)

@celery_app.task(bind=True)
def deity(self,url,name,pwd,data,data_zd):
    zz = Configure(url=url,name=name,pwd=pwd,data=data,data_zd=data_zd)
    self.update_state(state='PROGRESS',meta={'state': u'处理中', 'url': url})
    try:
        zz.run()
    except SSLError:
        return {'result': 'ok', 'url': url}
    return {'result': 'ok','url':url}


@celery_app.task(bind=True)
def updata(self, name, user_id):
    csv_reader = csv.reader(open('csv_/%s.csv' % name))
    error = 0
    with open('csv_/%s.csv' % name, 'r') as f:
        quantity = len(f.readlines())
    for id_,line in enumerate(csv_reader):
        self.update_state(state='PROGRESS', meta={'state': u'处理中', 'schedule': format(id_ / quantity * 100, '.2f'), 'error': '%s条异常' % error})
        time.sleep(2)
        if len(line) == 7:
            if line[0] != '标题' and line[0] and line[3] and line[5] and line[6]:
                if Subcategory.query.filter_by(auto_id=user_id).filter_by(id=line[6]).first():
                    try:
                        price = float(line[1])
                    except ValueError:
                        price = 0
                    data = Picture(name=line[0], price=price, attribute=line[2], picture=line[3],
                                   color=line[4], description=line[5], auto_id=user_id,subcategorys_id=line[6])
                    try:
                        db.session.add(data)
                        db.session.commit()
                    except Exception:
                        error += 1
                        db.session.rollback()
            else:
                error += 1
        else:
            error += 1
    return {'result': 'ok','state':u'运行成功'}
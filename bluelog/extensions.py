from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_nav import Nav
from flask_nav.elements import *
import redis
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_dropzone import Dropzone

debug = DebugToolbarExtension()
mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
nav = Nav()
dropzone = Dropzone()
pool = redis.ConnectionPool(host='119.91.128.205', port='6379', db=0, decode_responses=True)
r = redis.Redis(connection_pool=pool)


@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Auto
    user = Auto.query.get(int(user_id))
    return user

topbar = Navbar(u'数据管理系统0.1',
    View('主页', 'auto_manage.auto_manage_login'),
    Subgroup(
        '数据管理',
        View('大类', 'auto_manage.major_category', page='1'),
        View('小类', 'auto_manage.subcategory', page='1'),
        View('图片数据管理', 'auto_manage.picture_management', page='1'),
        Separator(),
        View('上传数据', 'csv.index', page='1')
    ),
    Subgroup(
        'CMS管理',
        View('关于我们', 'configuration.About_Us', page='1'),
        View('隐私及安全', 'configuration.Privacy_Security', page='1'),
        View('支付方式', 'configuration.Payment_Methods', page='1'),
        View('退货政策', 'configuration.Subcategory', page='1'),
        View('常问问题', 'configuration.Faq', page='1'),
        Separator(),
        View('基本设置', 'configuration.basicsettings', page='1'),
    ),
    View('配置网站', 'onebutton.index'),
    View('系统日志', 'csv.ruzhi'),
)
nav.register_element('top', topbar)
login_manager.login_view = 'auto.auto_login'
login_manager.login_message = u"请登陆"
login_manager.login_message_category = 'warning'

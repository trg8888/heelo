import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'tang1999')
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # BOOTSTRAP_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CSRF = True
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://new_user:Tang5230.@119.91.128.205/tongyi?charset=utf8'
    BLUELOG_POST_PER_PAGE = 10
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'wangyd1124@163.com'
    MAIL_PASSWORD = 'VSXDVGWNQOTVCSFE'
    ALBUMY_MAIL_SUBJECT_PREFIX = '数据'
    MAIL_DEFAULT_SENDER = ('数据',MAIL_USERNAME)
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = '.csv'
    DROPZONE_ENABLE_CSRF = True
    DEBUG = True
    ATTRIBUTE_BLANK = '-'  # 控制写入属性颜色跟属性中的地方
    MINIMUM = 1  # 最小写入数量
    MAXIMUM_NUMBER = 5 # 最大写入数量
    NAME = 'trg8888' # 解码平台账户
    PWD = 'trg8888' # 接码平台密码
    NAME_ID = '914366' # 接码平台ID


config = {
    'development': BaseConfig
}

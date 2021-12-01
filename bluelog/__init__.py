from flask import Flask
import os
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auto import auto_bp
from bluelog.extensions import db,csrf,bootstrap,login_manager,nav, mail, debug, dropzone
from bluelog.settings import config
from bluelog.blueprints.csv import csv_bp
from bluelog.blueprints.auto_manage import auto_manage_bp
from bluelog.blueprints.Siteconfiguration import configuration_bp
from bluelog.blueprints.Onebutton import onebutton_bp
from bluelog.fakes import fake_major,fake_subcategory,fake_picture_management,fake_about
from bluelog.tasks import celery_app
from bluelog.celeryconfig import celeryconfig

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    app = Flask('bluelog')
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    celery_app.config_from_object(celeryconfig)
    return app



def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    nav.init_app(app)
    mail.init_app(app)
    debug.init_app(app)
    dropzone.init_app(app)


def register_commands(app):
    @app.cli.command()
    def init():
        db.drop_all()
        db.create_all()
def register_blueprint(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auto_bp)
    app.register_blueprint(auto_manage_bp, url_prefix='/auto_manage')
    app.register_blueprint(configuration_bp,url_prefix='/configuration')
    app.register_blueprint(onebutton_bp,url_prefix='/onebutton')
    app.register_blueprint(csv_bp, url_prefix='/csv')



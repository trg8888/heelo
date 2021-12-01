from flask import Blueprint
from bluelog.tasks import add, flask_app_context
from bluelog.email import send_confirm_email

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/testAdd', methods=["GET"])
def test_add():
    """
    测试相加
    :return:
    """
    result = add.delay(1, 2)
    return result.get(timeout=1)


@admin_bp.route('/testFlaskAppContext', methods=["GET"])
def test_flask_app_context():
    """
    测试相加
    :return:
    """
    result = flask_app_context.delay()
    return result.get(timeout=1).replace('<Config', '')


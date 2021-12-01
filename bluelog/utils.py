from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bluelog.settings import Operations
from itsdangerous import BadSignature, SignatureExpired
from bluelog.models import Auto
from bluelog.extensions import db

def generate_token(email, operation, expire_in=None, **Kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'email':email, 'operation': operation}
    data.update(**Kwargs)
    return s.dumps(data)

def validate_token(token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    if operation != data.get('operation'):
        return False
    user = Auto.query.filter_by(email=data.get('email')).first()
    if operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if Auto.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    db.session.commit()
    return True
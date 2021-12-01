
from bluelog import create_app,celery_app

app = create_app()
app.debug = True
app.app_context().push()

from flask_wtf.csrf import  CSRFError

@app.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400

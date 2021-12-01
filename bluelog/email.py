
from bluelog.tasks import email_, updata
from bluelog.extensions import r

def send_confirm_email(email,subject, token,username, to=None):
    email_.delay(subject=subject, to=to or email, template='emails/confirm',username=username, token=token)

def updata_csv(name, user_id):
    task = updata.apply_async((name,user_id))
    r.lpush('error', task.id)
def data_updata_csv(data_id):
    task = updata.AsyncResult(data_id)
    if task.state == "PROGRESS":
        response = {
        'state':task.info.get('state',0),
        'schedule':task.info.get('schedule',0),
        'error':task.info.get('error',0)
    }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return response
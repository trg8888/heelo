class celeryconfig():
    broker_url = 'redis://119.91.128.205:6379/1'
    result_backend = 'redis://119.91.128.205:6379/2'
    timezone = 'Europe/Oslo'
    enable_utc = True
    include = ['bluelog.tasks']
    task_serializer = 'json'

    result_serializer = 'json'

    accept_content = ['json',]
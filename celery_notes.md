## Install redis
```bash
pipenv install redis
```
##install celery
```bash
pipenv install celery
```
## Run worker nodes
```bash
pipenv run python -m celery -A storefront worker --loglevel=info
```
## Configure(schedule tasks)--> `beats`
> `settings.py`
```python
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        # 'schedule':crontab(day_of_week=1, hour=7, minute=30)
        'schedule': 5,
        'args': ['Hello World'],
        # 'kwargs':{}
    }
}
```
### Run the beats (which the workers will be listening to)
```bash
pipenv run python -m celery -A storefront beats
```
## Monitor `celery` with `flower`
```bash
pipenv install flower
pipenv run python -m celery -A storefront flower
```



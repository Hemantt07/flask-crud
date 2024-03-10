from celery import Celery

celery = Celery(
    'application',
    backend = 'redis://localhost:6379/0',
    broker = 'redis://localhost:6379/0'
)

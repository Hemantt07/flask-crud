from application.background_tasks.celery_instance import celery

@celery.task
def add_numbers(x, y):
    return x + y
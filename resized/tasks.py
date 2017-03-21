from PIL import Image
from celery import Celery


celery_app = Celery('resized')
celery_app.config_from_object('resized.celeryconfig')


@celery_app.task
def scale_image(original, scaled):
    im = Image.open(original)
    im.thumbnail((96, 96))
    im.save(scaled, im.format)


def is_task_ready(task_id):
    r = celery_app.AsyncResult(task_id)
    return r.ready()

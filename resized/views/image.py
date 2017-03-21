from flask import Blueprint, url_for, send_file

from resized.tasks import is_task_ready
from resized.helpers import get_redis_conn


blueprint = Blueprint('image', __name__)


@blueprint.route('/image/scaled/<token>', methods=['GET'])
def get_scaled_image(token):
    r = get_redis_conn()
    path = r.hget('scaled', token)
    return send_file(path)


@blueprint.route('/image/original/<token>', methods=['GET'])
def get_original_image(token):
    r = get_redis_conn()
    path = r.hget('original', token)
    return send_file(path)


@blueprint.route('/image/<token>', methods=['GET'])
def get_images(token):

    href_original = url_for('image.get_original_image', token=token)
    if not is_task_ready(token):
        return '<img src="{0}">'.format(href_original)

    href_scaled = url_for('image.get_scaled_image', token=token)
    return '<img src="{0}"> <img src="{1}">'.format(href_original,
                                                    href_scaled)

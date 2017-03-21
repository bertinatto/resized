import os
import uuid

from flask import Blueprint, request, current_app

from resized.helpers import json_api, get_redis_conn
from resized.tasks import scale_image


blueprint = Blueprint('api', __name__)


@blueprint.route('/api/image', methods=['POST'])
@json_api
def upload_image():
    app = current_app._get_current_object()
    r = get_redis_conn()
    token = uuid.uuid4().hex

    # Normalize
    f = request.files['file']
    if f.filename == '':
        return dict(success=False)

    # Save original file
    original_path = os.path.join(app.config['UPLOAD_ORIGINAL'], token)
    f.save(original_path)

    # Start job
    scaled_path = os.path.join(app.config['UPLOAD_SCALED'], token)
    scale_image.apply_async((original_path, scaled_path), task_id=token)

    # Cache
    r.hset('original', token, original_path)
    r.hset('scaled', token, scaled_path)

    return {
        'success': True,
        'token': token
    }


@blueprint.route('/api/image/<token>', methods=['DELETE'])
def delete_image(token):
    r = get_redis_conn()

    for t in ('original', 'scaled'):
        path = r.hget(t, token)
        if not path:
            return 'not found', path
        try:
            os.remove(path)
        except OSError as e:
            return 'error' + e.msg

        r.hdel('original', token)

    return {'success': True}

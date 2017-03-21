from functools import wraps

import redis
from flask import jsonify, current_app


def get_redis_conn():
    app = current_app._get_current_object()
    return redis.StrictRedis(app.config['CACHE_HOST'],
                             decode_responses=True)


def json_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return jsonify(data)
    return wrapper

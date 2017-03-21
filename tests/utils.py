import pytest
# import redis

from flask import current_app as main_app


@pytest.fixture(scope="module")
def app():
    # main_app.config.from_object('TestingSettings')
    with main_app.app_context():
        return main_app.test_client()


# @pytest.fixture(scope="module")
# def test_client(app):
    # return app.test_client()


# @pytest.yield_fixture(scope="function")
# def cache_access(app):
    # """Flush entire cache."""
    # r = redis.StrictRedis(host=app.config['CACHE_HOST'], decode_responses=True)
    # yield
    # r.delete('original', 'scaled')

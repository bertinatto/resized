from flask import Flask

from resized import views


def create_app(config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    return app


def register_blueprints(app):
    app.register_blueprint(views.api.blueprint)
    app.register_blueprint(views.image.blueprint)


def register_extensions(app):
    pass


def register_error_handlers(app):
    pass

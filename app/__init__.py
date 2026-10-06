import os

from flask import Flask

from app.controllers import register_blueprints
from app.errors import register_error_handlers
from app.extensions import Base, create_session_factory


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(DATABASE_URL=os.environ.get("DATABASE_URL", "sqlite:///users.db"))
    if test_config:
        app.config.update(test_config)

    engine, session = create_session_factory(app.config["DATABASE_URL"])
    app.extensions["db_engine"] = engine
    app.extensions["db_session"] = session
    Base.metadata.create_all(engine)

    @app.teardown_appcontext
    def remove_session(_error=None):
        session.remove()

    register_blueprints(app)
    register_error_handlers(app)
    return app

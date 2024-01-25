import os

from flask import Flask
from database import init_db
import auth
from check_houses.h2s import holland2stay
from database import connection_string, shutdown_session


def create_app(test_config=None):
    print(create_app, 'asdasds')
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=connection_string,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(holland2stay.bp)

    app.teardown_appcontext(shutdown_session)

    # start the telegram bot
    with app.app_context():
        init_db()

    return app

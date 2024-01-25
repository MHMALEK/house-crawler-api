import os

from flask import Flask
from database import db
import auth
from check_houses.h2s import holland2stay


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        SQLALCHEMY_DATABASE_URI="sqlite:////" + os.path.join(app.instance_path, "flaskr.sqlite"),
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

    # start the telegram bot
    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
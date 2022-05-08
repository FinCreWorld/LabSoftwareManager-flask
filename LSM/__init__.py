import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE={
            "host": "127.0.0.1",
            "port": 3306,
            "database": "labsoftwaremanager",
            "password": "mysql",
            "user": "root",
            "charset": "utf8"
        }
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "hello world"

    from LSM import db
    db.init_app(app)

    from LSM import auth, room, lectures, softwares, teacher, computer
    app.register_blueprint(auth.bp)
    app.register_blueprint(room.bp)
    app.register_blueprint(lectures.bp)
    app.register_blueprint(softwares.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(computer.bp)

    @app.route("/")
    def root():
        return redirect(url_for("room.view"))

    return app

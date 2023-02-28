import os
from flask import Flask, redirect, render_template, session

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mi_secret_key',
        DATABASE_HOST='34.30.163.119',
        DATABASE_PORT='5432',
        DATABASE='postgres',
        DATABASE_USER='postgres',
        DATABASE_PASSWORD='pass_postgres'
    )

    # Postgres pass root: PostgresSQL_pass
    # app.config.from_mapping(
    #     SECRET_KEY='mi_secret_key',
    #     DATABASE_HOST='localhost',
    #     DATABASE_PORT='5432',
    #     DATABASE_USER='postgres',
    #     DATABASE_PASSWORD='PostgresSQL_pass',
    #     DATABASE='postgres'
    # )

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import bodega
    app.register_blueprint(bodega.bp)

    from . import administrativo
    app.register_blueprint(administrativo.bp)

    @app.route('/', methods=['POST', 'GET'])
    def hello():
        return render_template('saludo.html', tab=1)
        # return render_template('uno.html', tab=1)

    return app
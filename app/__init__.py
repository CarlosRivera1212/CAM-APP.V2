import os
from flask import Flask, redirect, render_template, session

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mi_secret_key',
        DATABASE_HOST='ec2-3-224-184-9.compute-1.amazonaws.com',
        DATABASE_PORT='5432',
        DATABASE_USER='fujztluotutykd',
        DATABASE_PASSWORD='f59705db149d9f0bebea3db84396a8cce3b303f7d3729d2cb4d6ef5950c74690',
        DATABASE='d2fvcanrcarno2'
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
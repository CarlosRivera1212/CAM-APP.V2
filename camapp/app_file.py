import os
from flask import Flask, redirect, render_template, session

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='mi_secret_key',
)

# app.config.from_mapping(
#     SECRET_KEY='mi_secret_key',
#     DATABASE_HOST='34.30.163.119',
#     DATABASE_PORT='5432',
#     DATABASE='postgres',
#     DATABASE_USER='postgres',
#     DATABASE_PASSWORD='pass_postgres'
# )

# Postgres pass root: PostgresSQL_pass
# app.config.from_mapping(
#     SECRET_KEY='mi_secret_key',
#     DATABASE_HOST='localhost',
#     DATABASE_PORT='5432',
#     DATABASE_USER='postgres',
#     DATABASE_PASSWORD='PostgresSQL_pass',
#     DATABASE='postgres'
# )

# import views
from routes.db import init_app
init_app(app)

from routes import auth, bodega, administrativo
app.register_blueprint(auth.bp)
app.register_blueprint(bodega.bp)
app.register_blueprint(administrativo.bp)

@app.route('/', methods=['POST', 'GET'])
def hello():
   return render_template('saludo.html', tab=1)
   # return 'Hello World!'


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)

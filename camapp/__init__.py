import os
from flask import Flask, redirect, render_template, session

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

import camapp.views

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)

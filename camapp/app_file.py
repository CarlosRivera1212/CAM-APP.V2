import os
from flask import Flask, redirect, render_template, session

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='mi_secret_key',
)

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


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)

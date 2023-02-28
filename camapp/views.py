from flask import Flask, redirect, render_template, session
from camapp import app

from camapp.db import init_app
init_app(app)

from camapp import auth, bodega, administrativo
app.register_blueprint(auth.bp)
app.register_blueprint(bodega.bp)
app.register_blueprint(administrativo.bp)

@app.route('/', methods=['POST', 'GET'])
def hello():
   return render_template('saludo.html', tab=1)
   # return 'Hello World!'
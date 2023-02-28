import functools
from flask import (
    Blueprint, flash, render_template, url_for, redirect, request, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from routes import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        usr = session.get('user_name')
        if usr is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = db.db_login(
            usr=request.form['username'].upper(),
            pwd=request.form['password']
        )

        if error is None:
            # db.db_load_prod()
            # db.db_load_activ()
            return redirect(url_for('hello'))
        
        flash(error)
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        new_user_name = '_'.join([
            request.form['username'],
            str(request.form['year']),
            request.form['semester'],
        ]).upper()

        msm = db.db_register(
            usr=new_user_name,
            pwd=request.form['password'],
            rol=request.form['role']
        )

        print(f'CREADO: {new_user_name}')
        flash(msm)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    # session['user_login'] = False
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    lusr = db.db_load_usr()
    
    if request.method == 'POST':
        if request.form['act'] == 'cam_psw':
            if request.form['pass_new1'] != request.form['pass_new2']:
                msm = 'Las nueva contraseña no coincide'
            else:
                msm, upt = db.db_update_pass(
                    usr=session['user_name'],
                    old_pwd=request.form['pass_curr'],
                    new_pwd=request.form['pass_new1']
                )
                if upt:
                    return redirect(url_for('auth.logout'))
        elif request.form['act'] == 'des':
            msm = db.db_update_activo(id_usr=request.form['user_des'])
        flash(msm)
    
    return render_template('auth/profile.html', tab = 6, list_usr = lusr)
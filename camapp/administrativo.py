from ast import Pass
from flask import (
    Blueprint, flash, render_template, url_for, redirect, request, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
from datetime import date

from . import db
from . import auth

bp = Blueprint('administrativo', __name__, url_prefix='/administrativo')


@bp.route('/cronograma', methods=['GET', 'POST'])
@auth.login_required
def cronograma():
    auxv = [date.today(), db.db_load_activ()]

    if request.method == 'POST':
        # nueva actividad
        if request.form['act'] == 'na':
            msm = db.db_nueva_actividad(
                id_grp=session['user_id'],
                act=request.form['activ'],
                des=request.form['descrip'],
                fec_p=request.form['fecha_progra'],
                tmp_p=request.form['tiemp_progra'],
                cos_p=request.form['costo_progra'],
                est=request.form['estado'],
            )
            flash(msm)
        # actividad realizada
        elif request.form['act'] == 'ar':
            msm1 = db.db_update_actividad(
                id_act=request.form['act_id'],
                fec_e=request.form['fecha_ejec'],
                tmp_e=request.form['tiemp_ejec'],
                est=request.form['estado'],
            )
            msm2 = db.db_update_venta(
                idu=request.form['venta'][1],
                ida=request.form['act_id'],
                fec_v=request.form['fecha_ejec']
            )
            msm3 = db.db_update_flujoc(
                idu=request.form['usr_id'],
                ida=request.form['act_id'],
                fec_prog=request.form['fecha_prog'],
                fec_ejec=request.form['fecha_ejec']
            )
            # # for m in msm2:
            # #     flash(m)
            flash(msm1)
            flash(msm2)
            flash(msm3)
        # nueva solicitad
        elif request.form['act'] == 'ns':
            valor_prod = [session['cart'][v]['prec'] for v in session['cart']]
            
            msm = db.db_nueva_solicitud(
                idgrp=session['user_id'],
                idact=request.form['activ_id'],
                fecsol=auxv[0],#request.form['fecsol'],
                prod_id=[pid for pid in session['cart']],
                prod=[pid['prod'][2] for pid in session['cart'].values()],
                cant=[pid['cant'] for pid in session['cart'].values()],
                # val=','.join([str(vi) for vi in valor_prod]),
                val=valor_prod, 
                valtot=session['cart_tot'],
                just=request.form['justif'],
                evi='NULL',
                doc=request.form['docente'],
                est='propuesto'
            )
            flash(msm)
        elif request.form['act'] == 'item_del':
            msm = db.db_del_activ(id_act=request.form['id_act'])
            flash(msm)
        else:
            flash('ERROR')
        
        return redirect(url_for('administrativo.cronograma'))

    return render_template('administrativo/cronograma.html', tab=4, hoy=auxv[0], list_activ=auxv[1])



@bp.route('/solicitudes', methods=['GET', 'POST'])
@auth.login_required
def solicitudes():
    auxv = [date.today(), db.db_load_solic()]
    if request.method == 'POST':
        # SOLICITUD RECHAZADA
        if request.form['act'] == 'aprob_solic':
            msm = db.db_update_solic(
                solic_id=request.form['solic_id'],
                solic_obs=request.form['observa'],
                estado='aprobado'
            )
        # SOLICITUD ACEPTADA
        elif request.form['act'] == 'recha_solic':
            msm = db.db_update_solic(
                solic_id=request.form['solic_id'],
                solic_obs=request.form['observa'],
                estado='rechazado',
                prod=request.form['solic_prod'],
                cant=request.form['solic_cant']
            )
        flash(msm)
        return redirect(url_for('administrativo.solicitudes'))
    return render_template('administrativo/solicitudes.html', tab = 2, list_solic=auxv[1])

@bp.route('/flujoc', methods=['GET', 'POST'])
@auth.login_required
def flujoc():
    auxv = [db.df_load_flujoc()]
    return render_template('administrativo/flujo_caja.html', tab = 5, list_fc=auxv[0])


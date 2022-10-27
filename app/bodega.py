from cgi import print_arguments
from flask import (
    Blueprint, flash, render_template, url_for, redirect, request, g, session,
    current_app
)

from . import db
from . import auth

bp = Blueprint('bodega', __name__, url_prefix='/bodega')


@bp.route('/tienda', methods=['GET', 'POST'])
@auth.login_required
def tienda(filt=None):
    auxv = [db.db_load_prod(), db.categ_prod()]
    
    if not 'cart' in session:
        session['cart'] = {}
    
    if request.method == 'GET':
        idc = request.args.get('idc')
        if not idc is None:
            if idc == '-1':
                session.pop('cart')
                session.pop('cart_tot')
                # session['cart_tot'] = 0
            else:
                session['cart'].pop(idc)
                prec_tot = [p['prec'] for p in session['cart'].values()]
                session['cart_tot'] = sum(prec_tot)

    elif request.method == 'POST':
        if request.form['act'] == 'np':
            msm = db.db_nuevo_producto(
                cat=request.form['categoria'],
                pro=request.form['producto'],
                des=request.form['descrip'],
                und=request.form['unidad'],
                ubi=request.form['ubicacion']
            )
            flash(msm)
        elif request.form['act'] == 'nc':
            msm = db.db_nueva_compra(
                pro=request.form['producto'],
                fch=request.form['fecha_compra'],
                fch_venc=request.form['fecha_vencimiento'],
                und=request.form['unidad'],
                cant=request.form['cantidad_compra'],
                vc_tot=request.form['valor_compra'],
                vc_und=request.form['valor_unidad'],
                vv_und=request.form['valor_venta']
            )
            flash(msm)
        elif request.form['act'] == 'item':
            # session['cart'] = session['cart']
            idp = int(request.form['prod_id'])
            prod_i = {
                'id': idp,
                'prod': [i for i in auxv[0] if i[0] == idp][0],
                'cant': float(request.form['cant']),
            }

            if prod_i['cant'] <= prod_i['prod'][5]:
                prod_i['prec'] = round(prod_i['prod'][6] * prod_i['cant'], 2)
                session['cart'][str(idp)] = prod_i
                prec_tot = [p['prec'] for p in session['cart'].values()]
                session['cart_tot'] = sum(prec_tot)
            else:
                flash('Cantidad Supera el Máximo')

        elif request.form['act'] == 'item_del':
            msm = db.db_del_prod(id_prod=request.form['prod_id'], prod=request.form['prod'])
            flash(msm)
        else:
            flash('ERROR')
        
        return redirect(url_for('bodega.tienda'))
    return render_template('bodega/tienda.html', tab=3, list_prod=auxv[0], categ_prod=auxv[1])

@bp.route('/solicitar_producto', methods=['GET', 'POST'])
@auth.login_required
def solicitar_producto():
    auxv = [db.db_load_prod(), db.categ_prod(), db.db_load_tienda_provi()]

    print(request.args.get)
    if not request.args.get('id_prov') is None:
        msm = db.db_del_tienda_provi(
            request.args.get('id_prov')
        )
        flash(msm)
        return redirect(url_for('bodega.solicitar_producto'))

    if request.method == 'POST':
        if request.form['act'] == 'snp':
            msm = db.db_tienda_provi(
                tipo=request.form['act'],
                campos=(
                    request.form['categoria'],
                    request.form['nomb_prod'],
                    request.form['desc_prod']
                )
            )
        elif request.form['act'] == 'rdp':
            msm = db.db_tienda_provi(
                tipo=request.form['act'],
                campos=(
                    request.form['nomb_prod'],
                    request.form['desc_prod']
                )
            )
        flash(msm)
        return redirect(url_for('bodega.solicitar_producto'))
        
    return render_template('bodega/solicitar_producto.html', list_prod=auxv[0], categ_prod=auxv[1], list_prov=auxv[2])


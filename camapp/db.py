import psycopg2
import click
from flask import redirect, url_for, current_app, g, session
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash, check_password_hash

from .static import schema

############################################################
############################################################
# INICIAR DB
############################################################
############################################################

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config['DATABASE_HOST'],
            port=current_app.config['DATABASE_PORT'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor()

    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for tblnm, sch in schema.crear_tablas.items():
        print(f"Creando: {tblnm}")
        for ins in sch:
            c.execute(ins)
        db.commit()
    print('Creando SUPERADMIN1')
    c.execute('INSERT INTO "usuario" (username, password, role) VALUES (%s, %s, %s)',
              ('SUPERADMIN1', generate_password_hash('CAMAPP_PASS_1'), 0))
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


############################################################
############################################################
# AUTH REQUEST
############################################################
############################################################

def db_login(usr, pwd):
    db, c = get_db()
    msm = None
    c.execute('SELECT * FROM "usuario" WHERE username = %s', (usr,))
    user = c.fetchone()
    if user is None:
        msm = 'Usuario y/o contraseña invalidos'
    elif not check_password_hash(user[2], pwd):
        msm = 'Usuario y/o contraseña invalidos'
    elif not user[4]:
        msm = 'Usuario INACTIVO'
    else:
        session.clear()
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_rol'] = user[3]
        session['user_login'] = True
    return msm

def db_register(usr, pwd, rol):
    db, c = get_db()
    msm = None
    c.execute('SELECT * FROM "usuario" WHERE username = %s', (usr,))
    if not c.fetchone() is None:
        msm = f'Usuario {usr} ya se encuentra registrado'
    else:
        c.execute(
            'INSERT INTO "usuario" (username, password, role) VALUES (%s, %s, %s);',
            (usr, generate_password_hash(pwd), rol)
        )
        db.commit()
        msm = f'Usuario {usr} registrado'
    return msm

def db_update_pass(usr, old_pwd, new_pwd):
    db, c = get_db()
    msm = None
    c.execute('SELECT * FROM "usuario" WHERE username = %s', (usr,))
    user = c.fetchone()
    
    if not check_password_hash(user[2], old_pwd):
        msm = 'Contraseña incorrecta'
        return msm, False
    else:
        c.execute(
            '''UPDATE "usuario"
            SET password = %s
            WHERE username=%s;''',
            (generate_password_hash(new_pwd), usr)
        )
        db.commit()
        msm = 'Contraseña Cambiada Exitosamente'
        return msm, True

def db_load_usr():
    db, c = get_db()
    c.execute(
        '''SELECT id, username
        FROM usuario
        WHERE role >= 2'''
    )
    lusr = c.fetchall()
    return lusr

def db_update_activo(id_usr):
    db, c = get_db()
    c.execute(
        '''UPDATE usuario
        SET activo = FALSE
        WHERE id = %s''',
        (id_usr,)
    )
    db.commit()
    msm = f'Usuario {id_usr} Desactivado'
    return msm

############################################################
############################################################
# BODEGA REQUEST
############################################################
############################################################

def db_del_prod(id_prod, prod):
    db, c = get_db()
    msm = None

    c.execute(
        '''DELETE FROM producto
        WHERE id = %s;''',
        (id_prod,)
    )
    db.commit()

    msm = f'Producto {id_prod}:{prod} Eliminado'
    return msm

def db_load_prod():
    db, c = get_db()
    c.execute('SELECT * FROM "producto" ORDER BY producto')
    lprod = c.fetchall()
    # session['list_prod'] = lprod
    # lprod_df = pd.DataFrame(
    #     lprod,
    #     columns=['id', 'categoria', 'subcategoria', 'producto', 'descrip',
    #              'unidad', 'cantidad_disp', 'valor_unid']
    # )
    return lprod

def db_nuevo_producto(cat, pro, des, und, ubi):
    db, c = get_db()
    msm = None
    c.execute('SELECT * FROM "producto" WHERE producto = %s', (pro,))
    if not c.fetchone() is None:
        msm = f'Producto {pro} ya se encuentra registrado'
    else:
        c.execute(
            '''INSERT INTO "producto"
            (categoria, producto, descrip, unidad,
            cantidad_disp, valor_unid, ubicacion,
            fecha_vencimiento, disponible)
            VALUES(%s,%s,%s,%s,0,0,%s,%s,%s);''',
            (cat, pro, des, und, ubi, 2022, 'NO')
        )
        db.commit()
        msm = f'Producto {pro} registrado'
    return msm

def db_nueva_compra(pro, fch, fch_venc, und, cant, vc_tot, vc_und, vv_und):
    db, c = get_db()
    msm = None

    c.execute(
        '''INSERT INTO "compra"
        (producto, fecha_compra, unidad, cantidad_compra,
        valor_compra, valor_unidad, valor_venta)
        VALUES(%s,%s,%s,%s,%s,%s,%s);''',
        (pro, fch, und, cant,
        vc_tot, vc_und, vv_und)
    )
    db.commit()
    db_update_cant_producto(
        prod=pro,
        cant=float(cant),
        val=float(vv_und),
        fven=float(fch_venc),
        tipo='compra'
    )

    msm = f'Compra {pro} registrada'
    return msm

def db_update_cant_producto(prod=None, cant=None, val=None, fven=None, tipo=None):
    db, c = get_db()

    c.execute('SELECT cantidad_disp FROM "producto" WHERE producto = %s;', (prod,))
    pre_cant = c.fetchone()[0]

    if tipo == 'compra':
        c.execute(
            '''UPDATE "producto"
            SET cantidad_disp = %s, valor_unid = %s, fecha_vencimiento = %s, disponible = %s
            WHERE producto=%s;''',
            (pre_cant+cant, val, fven, 'SI', prod)
        )
    elif tipo == 'solic':
        c.execute(
            '''UPDATE "producto"
            SET cantidad_disp = %s
            WHERE producto=%s;''',
            (pre_cant-cant, prod)
        )
    elif tipo == 'solic_rech':
        c.execute(
            '''UPDATE "producto"
            SET cantidad_disp = %s
            WHERE producto=%s;''',
            (pre_cant+cant, prod)
        )

    db.commit()

# TABLA PROVICIONAL
def db_tienda_provi(tipo, campos=None):
    db, c = get_db()
    msm = None
    
    if tipo == 'snp':
        c.execute(
            '''INSERT INTO provicional
            (tipo, c1, c2, c3)
            VALUES(%s,%s,%s,%s);''',
            (tipo,) + campos
        )
        db.commit()
        msm = f'NUEVO PRODUCTO SOLICITADO: {campos[1]}'
    elif tipo == 'del_snp':
        msm = 'BORRAR SOLICITUD NUEVO PRODUCTO'
    elif tipo == 'rdp':
        c.execute(
            '''INSERT INTO provicional
            (tipo, c1, c2)
            VALUES(%s,%s,%s);''',
            (tipo,) + campos
        )
        db.commit()
        c.execute(
            '''UPDATE "producto"
            SET disponible = %s
            WHERE producto=%s;''',
            ('NO', campos[0])
        )
        db.commit()
        msm = f'DAÑO PRODUCTO REPORTADO {campos[0]}'
    else:
        msm = 'Error'
    
    return msm

def db_del_tienda_provi(id):
    db, c = get_db()
    msm = None
    
    c.execute(
        '''DELETE FROM provicional
        WHERE id = %s;''',
        (id,)
    )
    db.commit()

    msm = f'{id} Eliminado'
    return msm

def db_load_tienda_provi():
    db, c = get_db()    
    c.execute(
        '''SELECT * FROM provicional'''
    )
    lprovi = c.fetchall()
    return lprovi
    
############################################################
############################################################
# CRONOGRAMA REQUEST
############################################################
############################################################

def db_del_activ(id_act):
    db, c = get_db()
    msm = None

    c.execute(
        '''DELETE FROM cronograma
        WHERE id = %s;''',
        (id_act,)
    )
    db.commit()

    msm = f'Actividad {id_act} Eliminada'
    return msm

def db_load_activ():
    db, c = get_db()
    
    rolgrp = session['user_rol']
    idgrp = session['user_id']
    
    if rolgrp == 3:
        c.execute(
            '''SELECT c.*, u.username, (
                SELECT COUNT(id) AS ns
                FROM solicitud AS s
                WHERE s.id_activ = c.id
            )
            FROM "cronograma" AS c
            LEFT JOIN "usuario" AS u
            ON c.id_usuario = u.id
            WHERE c.id_usuario = %s
            ORDER BY c.fecha_progra;''',
            (idgrp,)
        )
    else:
        c.execute(
            '''SELECT c.*, u.username, (
                SELECT COUNT(id) AS ns
                FROM solicitud AS s
                WHERE s.id_activ = c.id
            )
            FROM "cronograma" AS c
            LEFT JOIN "usuario" AS u
            ON c.id_usuario = u.id
            WHERE u.activo
            ORDER BY c.fecha_progra;'''
        )

    lactiv = c.fetchall()
    return lactiv

def db_nueva_actividad(id_grp, act, des, fec_p, tmp_p, cos_p, est):
    db, c = get_db()
    msm = None

    c.execute(
        '''INSERT INTO "cronograma"
        (id_usuario, actividad, descrip,
        fecha_progra, tiemp_progra, costo_progra,
        fecha_ejec, tiemp_ejec, costo_ejec,
        estado)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
        (id_grp, act, des, 
        fec_p, tmp_p, cos_p,
        fec_p, tmp_p, cos_p, est)
    )
    db.commit()

    msm = f'Actividad {act} registrada'
    return msm

def db_update_actividad(id_act, fec_e, tmp_e, est):
    db, c = get_db()

    c.execute(
        '''SELECT SUM(valor_tot)
        FROM solicitud
        WHERE id_activ = %s;''',
        (id_act,)
    )
    val_tot = float(c.fetchone()[0])
    
    c.execute(
        '''UPDATE "cronograma"
        SET fecha_ejec = %s, tiemp_ejec = %s, costo_ejec = %s, estado = %s
        WHERE id=%s;''',
        (fec_e, tmp_e, val_tot, est, id_act)
    )
    db.commit()
    msm = f'Actividad {id_act} Actualizada'
    return msm

############################################################
############################################################
# FLUJO DE CAJA REQUEST
############################################################
############################################################

# VENTAS

def db_update_venta(idu, ida, fec_v):
    db, c = get_db()
    msm = []
    
    c.execute(
        '''SELECT * from solicitud
        WHERE id_activ = %s;''',
        (ida,)
    )
    lsolic = c.fetchall()
    
    for sol in lsolic:
        ids = sol[0]
        prod = sol[4][1:-1].split(',')
        cant_v = sol[5][1:-1].split(',')
        unid_v = 'U'
        val_v = sol[6][1:-1].split(',')
        for pi, ci, vi in zip(prod, cant_v, val_v):
            c.execute(
                '''INSERT INTO "venta"
                (producto, id_usuario, id_solic, fecha_venta,
                cantidad_venta, unidad_venta, valor_venta)
                VALUES(%s,%s,%s,%s,%s,%s,%s);''',
                (pi, idu, ids, fec_v, ci, unid_v, vi)
            )
            db.commit()
            msm.append(f'Venta Registrada: {idu} - {pi}')

    return msm

# FLUJOC

def db_update_flujoc(idu, ida, fec_prog, fec_ejec):
    db, c = get_db()
    msm = []
    
    c.execute(
        '''SELECT SUM(valor_tot)
        FROM solicitud
        WHERE id_activ = %s;''',
        (ida,)
    )
    cost_ejec = c.fetchone()[0]
    
    c.execute(
        '''INSERT INTO "flujoc"
        (id_usuario, id_actividad,
        fecha_progra, fecha_ejec, costo_ejec)
        VALUES(%s,%s,%s,%s,%s);''',
        (idu, ida, fec_prog, fec_ejec, cost_ejec)
    )
    db.commit()
    msm = f'Flujo Caja Actualizado: {idu} - {ida}'
    return msm

def df_load_flujoc():
    db, c = get_db()
    
    rolgrp = session['user_rol']
    idgrp = session['user_id']
    
    if rolgrp == 3:
        c.execute(
            '''SELECT f.*, u.username, c.actividad
            FROM flujoc AS f
            LEFT JOIN usuario AS u
            ON f.id_usuario=u.id
            LEFT JOIN cronograma AS c
            ON f.id_actividad=c.id
            WHERE f.id_usuario = %s
            ORDER BY f.fecha_ejec;''',
            (idgrp,)
        )
    else:
        c.execute(
            '''SELECT f.*, u.username, c.actividad
            FROM flujoc AS f
            LEFT JOIN usuario AS u
            ON f.id_usuario=u.id
            LEFT JOIN cronograma AS c
            ON f.id_actividad=c.id
            ORDER BY f.fecha_ejec;'''
        )

    lflujoc = c.fetchall()
    return lflujoc


############################################################
############################################################
# SOLICITUD REQUEST
############################################################
############################################################

def db_load_solic():
    db, c = get_db()
    
    rolgrp = session['user_rol']
    idgrp = session['user_id']

    if rolgrp == 3:
        c.execute(
            '''SELECT s.*, u.username, c.actividad
            FROM "solicitud" AS s
            LEFT JOIN "usuario" AS u
            ON s.id_usuario = u.id
            LEFT JOIN "cronograma" AS c
            ON s.id_activ = c.id
            WHERE s.id_usuario = %s
            ORDER BY fecha_solic;''',
            (idgrp,)
        )
    else:
        c.execute(
            '''SELECT s.*, u.username, c.actividad
            FROM "solicitud" AS s
            LEFT JOIN "usuario" AS u
            ON s.id_usuario = u.id
            LEFT JOIN "cronograma" AS c
            ON s.id_activ = c.id
            WHERE u.activo
            ORDER BY fecha_solic;'''
        )

    lsolic = c.fetchall()
    return lsolic

def db_nueva_solicitud(idgrp, idact, fecsol, prod, cant, prod_id, val, valtot, just, evi, doc, est):
    db, c = get_db()
    msm = None
    
    c.execute(
        '''INSERT INTO "solicitud"
        (id_usuario, id_activ, fecha_solic,
        productos, cantidad, valor, valor_tot,
        justificacion, evidencia, docente, estado)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
        (idgrp, idact, fecsol, prod, cant, val, valtot, just, evi, doc, est)
    )
    db.commit()
    
    for pid in prod_id:
        db_update_cant_producto(
            prod=session['cart'][pid]['prod'][2],
            cant=session['cart'][pid]['cant'],
            tipo='solic'
        )
        db.commit()

    session.pop('cart')
    msm = f'Solicitud {idgrp}, {idact} Enviada'
    return msm

def db_update_solic(solic_id, solic_obs, estado, prod=None, cant=None):
    db, c = get_db()
    msm = None
    
    c.execute(
            '''UPDATE "solicitud"
            SET obser = %s, estado = %s
            WHERE id=%s;''',
            (solic_obs, estado, solic_id)
        )
    db.commit()
    if estado == 'rechazado':
        prod_s = prod[1:-1].split(',')
        cant_s = cant[1:-1].split(',')
        for p,c in zip(prod_s, cant_s):
            print(p,'---',c)
            db_update_cant_producto(
                prod=p,
                cant=float(c),
                tipo='solic_rech'
            )
            db.commit()

    msm = f'Solicitud: {solic_id} fue {estado}'
    return msm




def categ_prod():
    return [
        'ACARICIDA', 'AGENTE MICROBIANO', 'BACTERICIDA', 'BIOINSUMO',
        'COADYUVANTE', 'FERTILIZANTE ', 'FERTILIZANTE FOLIAR', 'FUNGICIDA',
        'HERBICIDA', 'HERRAMIENTA', 'INSECTICIDA', 'REGULADOR FISIOLOGICO'
    ]
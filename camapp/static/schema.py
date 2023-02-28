# INSTRUCCIONES PARA CREAR LAS TABLAS
# PASSWORD MYPOSTGRESQL: PostgresSQL_pass

crear_tablas = {
    # role: 0=superadmin, 1=admin, 2=auxiliar, 3=group
    'tabla_user': [
      'DROP TABLE IF EXISTS "usuario";',
      
      '''CREATE TABLE "usuario" (
        "id" SERIAL,
        "username" TEXT PRIMARY KEY UNIQUE NOT NULL,
        "password" TEXT NOT NULL,
        "role" INTEGER NOT NULL DEFAULT 3,
        "activo" BOOLEAN NOT NULL DEFAULT TRUE
      );'''
    ],
    'tabla_productos': [
      'DROP TABLE IF EXISTS "producto";',
      
      '''CREATE TABLE "producto" (
        "id" SERIAL PRIMARY KEY,
        "categoria" TEXT NOT NULL,
        "producto" TEXT UNIQUE NOT NULL,
        "descrip" TEXT NOT NULL,
        "unidad" TEXT NOT NULL,
        "cantidad_disp" FLOAT NOT NULL DEFAULT 0,
        "valor_unid" FLOAT NOT NULL DEFAULT 0,
        "ubicacion" TEXT NOT NULL,
        "fecha_vencimiento" FLOAT NOT NULL DEFAULT 0,
        "disponible" TEXT NOT NULL
      );'''
    ],
    'tabla_compras': [
      'DROP TABLE IF EXISTS "compra";',
      
      '''CREATE TABLE "compra" (
        "id" SERIAL PRIMARY KEY,
        "producto" TEXT NOT NULL,
        "fecha_compra" TEXT NOT NULL,
        "unidad" TEXT NOT NULL,
        "cantidad_compra" FLOAT NOT NULL,
        "valor_compra" FLOAT NOT NULL,
        "valor_unidad" FLOAT NOT NULL,
        "valor_venta" FLOAT NOT NULL
      );'''
    ],
    'tabla_ventas': [
      'DROP TABLE IF EXISTS "venta";',
      
      '''CREATE TABLE "venta" (
        "id" SERIAL PRIMARY KEY,
        "producto" TEXT NOT NULL,
        "id_usuario" INTEGER NOT NULL,
        "id_solic" INTEGER NOT NULL,
        "fecha_venta" TEXT NOT NULL,
        "cantidad_venta" FLOAT NOT NULL,
        "unidad_venta" TEXT NOT NULL,
        "valor_venta" FLOAT NOT NULL
      );'''
    ],
    # ESTADO: PROPUESTO, APROBADO, RECHAZADO
    'tabla_solici solicitud': [
      'DROP TABLE IF EXISTS "solicitud";',
      
      '''CREATE TABLE "solicitud" (
        "id" SERIAL PRIMARY KEY,
        "id_usuario" INTEGER NOT NULL,
        "id_activ" INTEGER NOT NULL,
        "fecha_solic" DATE NOT NULL,
        "productos" TEXT NOT NULL,
        "cantidad" TEXT NOT NULL,
        "valor" TEXT NOT NULL,
        "valor_tot" FLOAT NOT NULL,
        "justificacion" TEXT NOT NULL,
        "evidencia" TEXT,
        "docente" TEXT NOT NULL,
        "estado" TEXT NOT NULL,
        "obser" TEXT
    );'''
    ],
    'tabla_cronograma': [
      'DROP TABLE IF EXISTS "cronograma";',
      
      '''CREATE TABLE "cronograma" (
        "id" SERIAL PRIMARY KEY,
        "id_usuario" INTEGER NOT NULL,
        "actividad" TEXT NOT NULL,
        "descrip" TEXT NOT NULL,
        "fecha_progra" DATE NOT NULL,
        "tiemp_progra" FLOAT NOT NULL,
        "costo_progra" FLOAT NOT NULL,
        "fecha_ejec" DATE NOT NULL,
        "tiemp_ejec" FLOAT NOT NULL,
        "costo_ejec" FLOAT NOT NULL,
        "estado" TEXT NOT NULL
      );'''
    ],
    'tabla_flujoc': [
      'DROP TABLE IF EXISTS "flujoc";',
      
      '''CREATE TABLE "flujoc" (
        "id" SERIAL PRIMARY KEY,
        "id_usuario" INTEGER NOT NULL,
        "id_actividad" INTEGER NOT NULL,
        "fecha_progra" DATE NOT NULL,
        "fecha_ejec" DATE NOT NULL,
        "costo_ejec" FLOAT NOT NULL
      );'''
    ],
    'tabla_provicional': [
      'DROP TABLE IF EXISTS "provicional";',
      
      '''CREATE TABLE "provicional" (
        "id" SERIAL PRIMARY KEY,
        "tipo" TEXT,
        "c1" TEXT,
        "c2" TEXT,
        "c3" TEXT,
        "c4" TEXT,
        "c5" TEXT,
        "c6" TEXT
    );'''
    ]
}

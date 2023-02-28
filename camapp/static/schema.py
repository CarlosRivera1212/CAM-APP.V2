# INSTRUCCIONES PARA CREAR LAS TABLAS
# PASSWORD MYPOSTGRESQL: PostgresSQL_pass

crear_tablas = {
    # role: 0=superadmin, 1=admin, 2=auxiliar, 3=group
    'tabla_user': [
    'DROP TABLE IF EXISTS "usuario";',
    
    '''CREATE TABLE "usuario" (
      "id"	INTEGER,
      "username"	TEXT NOT NULL UNIQUE,
      "password"	TEXT NOT NULL,
      "role"	INTEGER NOT NULL DEFAULT 3,
      "activo"	BOOLEAN NOT NULL DEFAULT TRUE,
      PRIMARY KEY("id" AUTOINCREMENT)
      );'''
    ],
    'tabla_productos': [
      'DROP TABLE IF EXISTS "producto";',
      
      '''CREATE TABLE "producto" (
	"id"	INTEGER,
	"categoria"	TEXT NOT NULL,
	"producto"	TEXT NOT NULL UNIQUE,
	"descrip"	TEXT NOT NULL,
	"unidad"	TEXT NOT NULL,
	"cantidad_disp"	FLOAT NOT NULL DEFAULT 0,
	"valor_unid"	FLOAT NOT NULL DEFAULT 0,
	"ubicacion"	TEXT NOT NULL,
	"fecha_vencimiento"	FLOAT NOT NULL DEFAULT 0,
	"disponible"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    'tabla_compras': [
      'DROP TABLE IF EXISTS "compra";',
      
      '''CREATE TABLE "compra" (
	"id"	INTEGER,
	"producto"	TEXT NOT NULL,
	"fecha_compra"	TEXT NOT NULL,
	"unidad"	TEXT NOT NULL,
	"cantidad_compra"	FLOAT NOT NULL,
	"valor_compra"	FLOAT NOT NULL,
	"valor_unidad"	FLOAT NOT NULL,
	"valor_venta"	FLOAT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    'tabla_ventas': [
      'DROP TABLE IF EXISTS "venta";',
      
      '''CREATE TABLE "venta" (
	"id"	INTEGER,
	"producto"	TEXT NOT NULL,
	"id_usuario"	INTEGER NOT NULL,
	"id_solic"	INTEGER NOT NULL,
	"fecha_venta"	TEXT NOT NULL,
	"cantidad_venta"	FLOAT NOT NULL,
	"unidad_venta"	TEXT NOT NULL,
	"valor_venta"	FLOAT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    # ESTADO: PROPUESTO, APROBADO, RECHAZADO
    'tabla_solici solicitud': [
      'DROP TABLE IF EXISTS "solicitud";',
      
      '''CREATE TABLE "solicitud" (
	"id"	INTEGER,
	"id_usuario"	INTEGER NOT NULL,
	"id_activ"	INTEGER NOT NULL,
	"fecha_solic"	DATE NOT NULL,
	"productos"	TEXT NOT NULL,
	"cantidad"	TEXT NOT NULL,
	"valor"	TEXT NOT NULL,
	"valor_tot"	FLOAT NOT NULL,
	"justificacion"	TEXT NOT NULL,
	"evidencia"	TEXT,
	"docente"	TEXT NOT NULL,
	"estado"	TEXT NOT NULL,
	"obser"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    'tabla_cronograma': [
      'DROP TABLE IF EXISTS "cronograma";',
      
      '''CREATE TABLE "cronograma" (
	"id"	INTEGER,
	"id_usuario"	INTEGER NOT NULL,
	"actividad"	TEXT NOT NULL,
	"descrip"	TEXT NOT NULL,
	"fecha_progra"	DATE NOT NULL,
	"tiemp_progra"	FLOAT NOT NULL,
	"costo_progra"	FLOAT NOT NULL,
	"fecha_ejec"	DATE NOT NULL,
	"tiemp_ejec"	FLOAT NOT NULL,
	"costo_ejec"	FLOAT NOT NULL,
	"estado"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    'tabla_flujoc': [
      'DROP TABLE IF EXISTS "flujoc";',
      
      '''CREATE TABLE "flujoc" (
	"id"	INTEGER,
	"id_usuario"	INTEGER NOT NULL,
	"id_actividad"	INTEGER NOT NULL,
	"fecha_progra"	DATE NOT NULL,
	"fecha_ejec"	DATE NOT NULL,
	"costo_ejec"	FLOAT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ],
    'tabla_provicional': [
      'DROP TABLE IF EXISTS "provicional";',
      
      '''CREATE TABLE "provicional" (
	"id"	INTEGER,
	"tipo"	TEXT,
	"c1"	TEXT,
	"c2"	TEXT,
	"c3"	TEXT,
	"c4"	TEXT,
	"c5"	TEXT,
	"c6"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
    ]
}

import sqlite3

def conectar_db():
    return sqlite3.connect('venta.db')

def crear_tabla(query):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def ejecutar_consulta(query, params=()):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def ejecutar_modificacion(query, params=()):
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

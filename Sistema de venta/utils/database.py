import sqlite3

def conectar_db():
    conn = sqlite3.connect('ventass.db')
    return conn

def crear_tabla_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def mostrar_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

def buscar_producto(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, precio, cantidad FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    return producto

# Otras funciones para interactuar con la base de datos
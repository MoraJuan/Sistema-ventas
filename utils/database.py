import sqlite3

def conectar_db():
    conn = sqlite3.connect('venta.db')
    return conn

def crear_tabla_usuarios():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

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

def buscar_usuario(usuario):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def insertar_usuario(usuario, contrasena):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena))
    conn.commit()
    conn.close()


def buscar_producto_por_nombre_bd(nombre):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, precio, cantidad FROM productos WHERE nombre LIKE ?', ('%' + nombre + '%',))
    productos = cursor.fetchall()
    conn.close()
    return productos

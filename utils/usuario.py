from utils.database import ejecutar_consulta, ejecutar_modificacion, crear_tabla

def crear_tabla_usuarios():
    query = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    '''
    crear_tabla(query)

def buscar_usuario(usuario):
    query = 'SELECT * FROM usuarios WHERE usuario = ?'
    resultado = ejecutar_consulta(query, (usuario,))
    return resultado[0] if resultado else None

def insertar_usuario(usuario, contrasena):
    query = 'INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)'
    ejecutar_modificacion(query, (usuario, contrasena))
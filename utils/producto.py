from utils.database import ejecutar_consulta, crear_tabla

def crear_tabla_productos():
    query = '''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre STRING NOT NULL,
            precio FLOAT NOT NULL,
            cantidad INTEGER NOT NULL
        )
    '''
    crear_tabla(query)

def mostrar_productos ():
    query = 'SELECT * FROM productos'
    resultado = ejecutar_consulta (query)
    return resultado

def buscar_producto_por_nombre_bd(nombre):
    query = 'SELECT * FROM productos WHERE nombre = ?'
    resultado = ejecutar_consulta(query, (nombre,))
    return resultado if resultado else []

def buscar_producto (id):
    query='SELECT * FROM productos WHERE id=?'
    resultado = ejecutar_consulta(query, (id,))
    return resultado if resultado else []

# buscar_producto, buscar_producto_por_nombre_bd
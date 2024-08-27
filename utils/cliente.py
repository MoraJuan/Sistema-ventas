from utils.database import ejecutar_consulta, crear_tabla

def crear_tabla_cliente():
    query = '''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre STRING NOT NULL,
            mail STRING NOT NULL,
            telefono STRING NOT NULL
        )
    '''
    crear_tabla(query)

def mostrar_clientes():
    query = 'SELECT * FROM clientes'
    resultado = ejecutar_consulta(query)
    return resultado

def buscar_cliente_por_nombre_bd(nombre):
    query = 'SELECT * FROM clientes WHERE nombre = ?'
    resultado = ejecutar_consulta(query, (nombre,))
    return resultado if resultado else []
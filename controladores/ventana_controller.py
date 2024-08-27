def calcular_total(productos):
    total = 0
    print(productos)
    for producto in productos:
        total += producto.precio * producto.cantidad  # Suponiendo que productos es una lista de tuplas (nombre, precio)
    return total

# Otras funciones de lógica de negocio relacionadas con las ventas
def calcular_total(productos):
    total = 0
    print(productos)
    for producto in productos:
        print(producto[1])
        total += producto[1]  # Suponiendo que productos es una lista de tuplas (nombre, precio)
    return total

# Otras funciones de lógica de negocio relacionadas con las ventas
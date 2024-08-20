class Producto:
    nombre = ""
    precio = 0.0
    cantidad = 0
    def __init__(self, nombre, precio, cantidad=1):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.precio * self.cantidad
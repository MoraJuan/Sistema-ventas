import sys
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from controladores.ventana_controller import calcular_total
from utils.database import buscar_producto


class VentanaCobro(QMainWindow):
    def __init__(self, productos):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas")
        self.setGeometry(100, 100, 800, 600)

        self.productos = productos
        self.carrito = []

        self.crear_widgets()
        self.crear_layout()
        self.actualizar_tabla()

    def crear_widgets(self):
        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(3)
        self.tabla_productos.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad"])
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Búsqueda de producto
        self.label_buscar_producto = QLabel("Buscar Producto por ID:")
        self.entrada_buscar_producto = QLineEdit()
        self.boton_buscar_producto = QPushButton("Buscar")
        self.boton_buscar_producto.clicked.connect(self.buscar_producto)

        # Botones de acción
        self.boton_finalizar = QPushButton("Finalizar Venta")
        self.boton_finalizar.clicked.connect(self.finalizar_venta)
        self.boton_cancelar = QPushButton("Cancelar Venta")
        self.boton_cancelar.clicked.connect(self.cancelar_venta)
        self.boton_agregar_carrito = QPushButton("Agregar al Carrito")
        self.boton_agregar_carrito.clicked.connect(self.agregar_al_carrito)
        self.boton_limpiar_carrito = QPushButton("Limpiar Carrito")
        self.boton_limpiar_carrito.clicked.connect(self.limpiar_carrito)

        # Aplicar estilos a los botones
        self.estilizar_botones()

    def estilizar_botones(self):
        estilo_boton = """
        QPushButton {
            background-color: #4CAF50; /* Verde */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        self.boton_finalizar.setStyleSheet(estilo_boton)
        self.boton_cancelar.setStyleSheet(estilo_boton)
        self.boton_agregar_carrito.setStyleSheet(estilo_boton)
        self.boton_limpiar_carrito.setStyleSheet(estilo_boton)
        self.boton_buscar_producto.setStyleSheet(estilo_boton)

    def crear_layout(self):
        layout_principal = QVBoxLayout()

        # Sección de búsqueda
        layout_buscar = QHBoxLayout()
        layout_buscar.addWidget(self.label_buscar_producto)
        layout_buscar.addWidget(self.entrada_buscar_producto)
        layout_buscar.addWidget(self.boton_buscar_producto)
        layout_principal.addLayout(layout_buscar)

        # Tabla de productos
        layout_principal.addWidget(self.tabla_productos)

        # Botones de acción
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_finalizar)
        layout_botones.addWidget(self.boton_cancelar)
        layout_botones.addStretch(1)  # Espacio flexible
        layout_botones.addWidget(self.boton_agregar_carrito)
        layout_botones.addWidget(self.boton_limpiar_carrito)
        layout_principal.addLayout(layout_botones)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    def actualizar_tabla(self):
        self.tabla_productos.setRowCount(len(self.productos))
        for fila, producto in enumerate(self.productos):
            if len(producto) == 3:
                nombre, precio, cantidad = producto
                self.tabla_productos.setItem(fila, 0, QTableWidgetItem(nombre))
                self.tabla_productos.setItem(fila, 1, QTableWidgetItem(str(precio)))
                self.tabla_productos.setItem(fila, 2, QTableWidgetItem(str(cantidad)))

    def buscar_producto(self):
        id_text = self.entrada_buscar_producto.text()
        if not id_text.isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingresa un ID válido.")
            return

        id = int(id_text)
        producto = buscar_producto(id)
        if producto:
            if len(producto) == 3:
                self.productos = [producto] 
                self.actualizar_tabla()
            else:
                QMessageBox.warning(self, "Error", "El formato del producto es incorrecto.")
        else:
            QMessageBox.warning(self, "Error", "Producto no encontrado.")

    def agregar_al_carrito(self):
        if self.productos:
            self.carrito.extend(self.productos)
            QMessageBox.information(self, "Carrito", "Producto(s) agregado(s) al carrito.")
            self.productos = []  # Limpiar la tabla después de agregar
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "No hay productos para agregar al carrito.")

    def limpiar_carrito(self):
        self.carrito = []
        QMessageBox.information(self, "Carrito", "Carrito limpiado.")

    def finalizar_venta(self):
        if self.carrito:
            total = calcular_total(self.carrito)
            QMessageBox.information(self, "Venta Finalizada", f"Total: ${total:.2f}")
            self.carrito = []
            # Puedes agregar aquí la lógica para registrar la venta en la base de datos
            self.actualizar_tabla() 
        else:
            QMessageBox.warning(self, "Error", "No hay productos en el carrito.")

    def cancelar_venta(self):
        if self.productos or self.carrito:
            respuesta = QMessageBox.question(
                self, "Cancelar Venta", "¿Estás seguro de que quieres cancelar la venta?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.productos = []
                self.carrito = []
                self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "No hay productos en la venta ni en el carrito.")

    def volver_al_inicio(self):
        self.close()
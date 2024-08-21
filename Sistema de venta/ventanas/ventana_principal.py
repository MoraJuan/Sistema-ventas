import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from controladores.ventana_controller import calcular_total
from utils.database import crear_tabla_productos
from ventanas.ventanaCobro import VentanaCobro
from ventanas.ventanaVentas import VentanaVentas

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas - Menú Principal")
        self.setGeometry(300, 300, 400, 200)

        # Crear la tabla de productos si no existe
        crear_tabla_productos()

        self.crear_widgets()
        self.crear_layout()

        # Aplicar estilos CSS a los botones
        self.boton_agregar_producto.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Color de fondo verde */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px; /* Bordes redondeados */
            }
            QPushButton:hover {
                background-color: #3e8e41; /* Color más oscuro al pasar el mouse */
            }
        """)

        self.boton_realizar_cobro.setStyleSheet("""
            QPushButton {
                background-color: #008CBA; /* Color de fondo azul */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px; /* Bordes redondeados */
            }
            QPushButton:hover {
                background-color: #00688B; /* Color más oscuro al pasar el mouse */
            }
        """)

    def crear_widgets(self):
        self.boton_agregar_producto = QPushButton("Agregar Producto / Eliminar Producto", self)
        self.boton_agregar_producto.clicked.connect(self.abrir_ventana_agregar_producto)

        self.boton_realizar_cobro = QPushButton("Realizar Cobro", self)
        self.boton_realizar_cobro.clicked.connect(self.abrir_ventana_realizar_cobro)

        self.label_estado = QLabel("Estado: Listo", self)

    def crear_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.boton_agregar_producto)
        layout.addWidget(self.boton_realizar_cobro)
        layout.addWidget(self.label_estado) 

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_ventana_agregar_producto(self):
        self.ventana_ventas = VentanaVentas()
        self.ventana_ventas.show()

    def abrir_ventana_realizar_cobro(self):
        if hasattr(self, 'ventana_ventas') and self.ventana_ventas.productos:
            self.ventana_cobro = VentanaCobro(self.ventana_ventas.productos)
            self.ventana_cobro.show()
        else:
            QMessageBox.warning(self, "Error", "No hay productos para cobrar.")
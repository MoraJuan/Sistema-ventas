from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt  
from utils.producto import crear_tabla_productos
from ventanas.ventanaCobro import VentanaCobro
from ventanas.ventanaVentas import VentanaVentas
from ventanas.ventanaCliente import VentanaCliente

class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Sistema de Ventas - Menú Principal")
        self.showMaximized()

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

        self.boton_agregar_cliente.setStyleSheet("""
            QPushButton {
                background-color: #f44336; /* Color de fondo rojo */
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
                background-color: #d32f2f; /* Color más oscuro al pasar el mouse */
            }
        """)

        # Aplicar estilos CSS al widget central
        self.centralWidget().setStyleSheet("""
            background-color: #f2f2f2; /* Color de fondo gris claro */
            border-radius: 10px; /* Bordes redondeados */
            padding: 20px;
        """)

    def crear_widgets(self):
        self.label_usuario = QLabel(f"Bienvenido, {self.usuario}!", self)
        self.label_usuario.setAlignment(Qt.AlignCenter)
        self.label_usuario.setStyleSheet("font-size: 18px; margin-bottom: 20px;")

        self.boton_agregar_producto = QPushButton("Agregar Producto / Eliminar Producto", self)
        self.boton_agregar_producto.clicked.connect(self.abrir_ventana_agregar_producto)

        self.boton_realizar_cobro = QPushButton("Realizar Cobro", self)
        self.boton_realizar_cobro.clicked.connect(self.abrir_ventana_realizar_cobro)

        self.boton_agregar_cliente = QPushButton("Agregar Cliente", self)
        self.boton_agregar_cliente.clicked.connect(self.abrir_ventana_agregar_cliente)

    def crear_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.boton_agregar_producto)
        layout.addWidget(self.boton_realizar_cobro)
        layout.addWidget(self.boton_agregar_cliente)

        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def abrir_ventana_agregar_producto(self):
        self.ventana_ventas = VentanaVentas()
        self.ventana_ventas.show()

    def abrir_ventana_realizar_cobro(self):
        self.ventana_cobro = VentanaCobro()
        self.ventana_cobro.show()
    
    def abrir_ventana_agregar_cliente(self):
        self.ventana_usuario = VentanaCliente()
        self.ventana_usuario.show()

from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt

from utils.usuario import buscar_usuario, insertar_usuario

class VentanaCrearUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear Usuario")
        self.setGeometry(100, 100, 400, 300)

        self.crear_widgets()
        self.crear_layout()
        self.aplicar_estilos()

    def crear_widgets(self):
        self.label_usuario = QLabel("Nuevo Usuario:")
        self.entrada_usuario = QLineEdit()

        self.label_contrasena = QLabel("Contraseña:")
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setEchoMode(QLineEdit.Password)

        self.label_confirmar_contrasena = QLabel("Confirmar Contraseña:")
        self.entrada_confirmar_contrasena = QLineEdit()
        self.entrada_confirmar_contrasena.setEchoMode(QLineEdit.Password)

        self.boton_crear_usuario = QPushButton("Crear Usuario")
        self.boton_crear_usuario.clicked.connect(self.crear_usuario)

    def crear_layout(self):
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.label_usuario)
        layout_principal.addWidget(self.entrada_usuario)
        layout_principal.addWidget(self.label_contrasena)
        layout_principal.addWidget(self.entrada_contrasena)
        layout_principal.addWidget(self.label_confirmar_contrasena)
        layout_principal.addWidget(self.entrada_confirmar_contrasena)
        layout_principal.addWidget(self.boton_crear_usuario)

        layout_principal.setAlignment(Qt.AlignCenter)
        layout_principal.setSpacing(15)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QLineEdit {
                font-size: 16px;
                padding: 5px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def crear_usuario(self):
        usuario = self.entrada_usuario.text()
        contrasena = self.entrada_contrasena.text()
        confirmar_contrasena = self.entrada_confirmar_contrasena.text()

        if contrasena != confirmar_contrasena:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        if buscar_usuario(usuario):
            QMessageBox.warning(self, "Error", "El usuario ya existe.")
            return

        insertar_usuario(usuario, contrasena)
        QMessageBox.information(self, "Éxito", "Usuario creado exitosamente.")
        self.abrir_ventana_inicio()

    def abrir_ventana_inicio(self):
        from ventanas.landing.ventana_inicio import VentanaInicio
        self.ventana_inicio = VentanaInicio()
        self.ventana_inicio.show()
        self.close()



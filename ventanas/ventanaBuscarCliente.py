from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from utils.cliente import buscar_cliente_por_nombre_bd

class VentanaBuscarCliente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar Cliente")
        self.setFixedSize(300, 150)

        self.etiqueta_nombre = QLabel("Nombre:")
        self.entrada_nombre = QLineEdit()
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_cliente)

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta_nombre)
        layout.addWidget(self.entrada_nombre)
        layout.addWidget(self.boton_buscar)
        self.setLayout(layout)

        self.resultado_busqueda = None

    def buscar_cliente(self):
        nombre = self.entrada_nombre.text()
        if nombre:
            cliente = buscar_cliente_por_nombre_bd(nombre)
            if cliente:
                self.resultado_busqueda = cliente
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Cliente no encontrado.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingresa el nombre del cliente.")
# ventanas/ventanaCliente.py

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QWidget
from utils.database import conectar_db
from utils.cliente import mostrar_clientes, crear_tabla_cliente

class VentanaCliente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        self.showMaximized()

        self.clientes = []

        crear_tabla_cliente()  # Crear la tabla clientes si no existe
        self.crear_widgets()
        self.crear_layout()
        self.cargar_clientes()  # Cargar clientes desde la base de datos al iniciar

    def crear_widgets(self):
        # Widgets para agregar clientes
        self.etiqueta_nombre = QLabel("Nombre:")
        self.entrada_nombre = QLineEdit()
        self.etiqueta_mail = QLabel("Email:")
        self.entrada_mail = QLineEdit()
        self.etiqueta_telefono = QLabel("Teléfono:")
        self.entrada_telefono = QLineEdit()
        self.boton_agregar = QPushButton("Agregar Cliente")
        self.boton_agregar.clicked.connect(self.agregar_cliente)
        self.boton_eliminar_seleccionado = QPushButton("Eliminar Cliente Seleccionado")
        self.boton_eliminar_seleccionado.clicked.connect(self.eliminar_cliente_seleccionado)

        # Tabla para mostrar los clientes
        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(4)
        self.tabla_clientes.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Teléfono"])

        # Botones para finalizar la gestión de clientes
        self.boton_finalizar = QPushButton("Volver al Inicio")
        self.boton_finalizar.clicked.connect(self.volver_al_inicio)

        # Aplicar estilos a los widgets
        self.aplicar_estilos()

    def crear_layout(self):
        layout_principal = QVBoxLayout()

        # Layout para agregar clientes
        layout_agregar = QHBoxLayout()
        layout_agregar.addWidget(self.etiqueta_nombre)
        layout_agregar.addWidget(self.entrada_nombre)
        layout_agregar.addWidget(self.etiqueta_mail)
        layout_agregar.addWidget(self.entrada_mail)
        layout_agregar.addWidget(self.etiqueta_telefono)
        layout_agregar.addWidget(self.entrada_telefono)  # Asegúrate de añadir el campo de teléfono
        layout_agregar.addWidget(self.boton_agregar)
        layout_principal.addLayout(layout_agregar)

        # Agregamos la tabla de clientes
        layout_principal.addWidget(self.tabla_clientes)

        # Layout para los botones de abajo
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_eliminar_seleccionado)
        layout_botones.addWidget(self.boton_finalizar)
        layout_principal.addLayout(layout_botones)

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    def aplicar_estilos(self):
        # Estilos para las etiquetas
        estilo_etiqueta = "font-size: 14px; font-weight: bold;"
        self.etiqueta_nombre.setStyleSheet(estilo_etiqueta)
        self.etiqueta_mail.setStyleSheet(estilo_etiqueta)
        self.etiqueta_telefono.setStyleSheet(estilo_etiqueta)

        # Estilos para las entradas de texto
        estilo_entrada = "padding: 5px; font-size: 14px;"
        self.entrada_nombre.setStyleSheet(estilo_entrada)
        self.entrada_mail.setStyleSheet(estilo_entrada)
        self.entrada_telefono.setStyleSheet(estilo_entrada)

        # Estilos para los botones
        estilo_boton = """
            QPushButton {
                background-color: #4CAF50; /* Color de fondo verde */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px; /* Bordes redondeados */
            }
            QPushButton:hover {
                background-color: #45a049; /* Color más oscuro al pasar el mouse */
            }
        """
        self.boton_agregar.setStyleSheet(estilo_boton)
        self.boton_eliminar_seleccionado.setStyleSheet(estilo_boton)
        self.boton_finalizar.setStyleSheet(estilo_boton)

        # Estilos para la tabla
        estilo_tabla = """
            QTableWidget {
                gridline-color: #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f3f3f3;
                padding: 4px;
                border: 1px solid #ddd;
                font-size: 14px;
                font-weight: bold;
            }
        """
        self.tabla_clientes.setStyleSheet(estilo_tabla)

    def agregar_cliente(self):
        nombre = self.entrada_nombre.text()
        mail = self.entrada_mail.text()
        telefono = self.entrada_telefono.text()

        if nombre and mail and telefono:
            try:
                # Insertamos el cliente en la base de datos
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nombre, mail, telefono) VALUES (?, ?, ?)", (nombre, mail, telefono))
                conn.commit()

                # Obtenemos el ID del cliente recién insertado
                cursor.execute("SELECT last_insert_rowid()")
                cliente_id = cursor.fetchone()[0]
                conn.close()

                self.clientes.append((cliente_id, nombre, mail, telefono))
                self.actualizar_tabla()
                self.entrada_nombre.clear()
                self.entrada_mail.clear()
                self.entrada_telefono.clear()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al agregar el cliente: {e}")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingresa el nombre, email y teléfono.")

    def actualizar_tabla(self):
        self.tabla_clientes.setRowCount(len(self.clientes))
        for fila, (cliente_id, nombre, mail, telefono) in enumerate(self.clientes):
            self.tabla_clientes.setItem(fila, 0, QTableWidgetItem(str(cliente_id)))
            self.tabla_clientes.setItem(fila, 1, QTableWidgetItem(nombre))
            self.tabla_clientes.setItem(fila, 2, QTableWidgetItem(mail))
            self.tabla_clientes.setItem(fila, 3, QTableWidgetItem(telefono))

    def cargar_clientes(self):
        clientes_db = mostrar_clientes()
        self.clientes = [(cliente[0], cliente[1], cliente[2], cliente[3]) for cliente in clientes_db]
        self.actualizar_tabla()

    def eliminar_cliente_seleccionado(self):
        fila_seleccionada = self.tabla_clientes.currentRow()
        if fila_seleccionada != -1:
            cliente = self.clientes.pop(fila_seleccionada)
            self.actualizar_tabla()

            # Eliminar el cliente seleccionado de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente[0],))
            conn.commit()
            conn.close()
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un cliente para eliminar.")

    def volver_al_inicio(self):
        self.close()
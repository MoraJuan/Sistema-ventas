from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget, QDialog
from utils.database import conectar_db
from utils.cliente import mostrar_clientes, crear_tabla_cliente, buscar_cliente_por_nombre_bd
from ventanas.ventanaBuscarCliente import VentanaBuscarCliente
import csv 
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

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
        self.boton_buscar = QPushButton("Buscar Cliente")
        self.boton_buscar.clicked.connect(self.abrir_ventana_buscar_cliente)
        self.boton_editar = QPushButton("Editar Cliente")
        self.boton_editar.clicked.connect(self.editar_cliente)
        self.boton_exportar = QPushButton("Exportar a CSV")
        self.boton_exportar.clicked.connect(self.exportar_clientes_csv)
        self.boton_importar = QPushButton("Importar desde CSV")
        self.boton_importar.clicked.connect(self.importar_clientes_csv)

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
      
        layout_botones.addWidget(self.boton_eliminar_seleccionado)
        layout_botones.addWidget(self.boton_buscar)
        layout_botones.addWidget(self.boton_editar)          # Nuevo botón
        layout_botones.addWidget(self.boton_exportar)        # Nuevo botón
        layout_botones.addWidget(self.boton_importar)        # Nuevo botón
        layout_botones.addWidget(self.boton_finalizar)
        layout_principal.addLayout(layout_botones)

        # Agregamos la tabla de clientes
        layout_principal.addWidget(self.tabla_clientes)

        # Layout para los botones de abajo
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_eliminar_seleccionado)
        layout_botones.addWidget(self.boton_buscar)
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
        self.boton_buscar.setStyleSheet(estilo_boton)
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
            self.tabla_clientes.setItem(fila, 3, QTableWidgetItem(str(telefono)))

    def cargar_clientes(self):
        clientes_db = mostrar_clientes()
        print("Clientes cargados desde la base de datos:", clientes_db)  # Mensaje de depuración
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
    
    def abrir_ventana_buscar_cliente(self):
        ventana_buscar = VentanaBuscarCliente(self)
        if ventana_buscar.exec_() == QDialog.Accepted:
            self.clientes = ventana_buscar.resultado_busqueda
            self.actualizar_tabla()
    
    def editar_cliente(self):
        fila_seleccionada = self.tabla_clientes.currentRow()
        if fila_seleccionada != -1:
            cliente = self.clientes[fila_seleccionada]
            dialog = EditarClienteDialog(cliente, self)
            if dialog.exec_() == QDialog.Accepted:
                datos_actualizados = dialog.obtener_datos()
                try:
                    conn = conectar_db()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE clientes SET nombre = ?, mail = ?, telefono = ? WHERE id = ?",
                                (datos_actualizados['nombre'], datos_actualizados['mail'],
                                    datos_actualizados['telefono'], cliente[0]))
                    conn.commit()
                    conn.close()

                    self.clientes[fila_seleccionada] = (
                        cliente[0],
                        datos_actualizados['nombre'],
                        datos_actualizados['mail'],
                        datos_actualizados['telefono']
                    )
                    self.actualizar_tabla()
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error al actualizar el cliente: {e}")
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un cliente para editar.")
    def importar_clientes_csv(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Importar Clientes desde CSV", "", "CSV Files (*.csv)")
        if ruta_archivo:
            try:
                with open(ruta_archivo, mode='r', encoding='utf-8') as archivo_csv:
                    lector = csv.DictReader(archivo_csv)
                    clientes_importados = []
                    conn = conectar_db()
                    cursor = conn.cursor()
                    for fila in lector:
                        nombre = fila['Nombre']
                        mail = fila['Email']
                        telefono = fila['Teléfono']
                        cursor.execute("INSERT INTO clientes (nombre, mail, telefono) VALUES (?, ?, ?)", (nombre, mail, telefono))
                        clientes_importados.append((cursor.lastrowid, nombre, mail, telefono))
                    conn.commit()
                    conn.close()
                
                self.clientes.extend(clientes_importados)
                self.actualizar_tabla()
                QMessageBox.information(self, "Éxito", "Clientes importados correctamente desde CSV.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al importar desde CSV: {e}")
    def exportar_clientes_csv(self):
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Exportar Clientes a CSV", "", "CSV Files (*.csv)")
        if ruta_archivo:
            try:
                with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo_csv:
                    campos = ['ID', 'Nombre', 'Email', 'Teléfono']
                    escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
                    escritor.writeheader()
                    for cliente in self.clientes:
                        escritor.writerow({
                            'ID': cliente[0],
                            'Nombre': cliente[1],
                            'Email': cliente[2],
                            'Teléfono': cliente[3]
                        })
                QMessageBox.information(self, "Éxito", "Clientes exportados correctamente a CSV.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al exportar a CSV: {e}")

    class EditarClienteDialog(QDialog):
        def __init__(self, cliente, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Editar Cliente")
            self.cliente = cliente
            self.init_ui()

        def init_ui(self):
            layout = QVBoxLayout()

            # Nombre
            self.label_nombre = QLabel("Nombre:")
            self.input_nombre = QLineEdit(self.cliente[1])
            layout.addWidget(self.label_nombre)
            layout.addWidget(self.input_nombre)

            # Email
            self.label_mail = QLabel("Email:")
            self.input_mail = QLineEdit(self.cliente[2])
            layout.addWidget(self.label_mail)
            layout.addWidget(self.input_mail)

            # Teléfono
            self.label_telefono = QLabel("Teléfono:")
            self.input_telefono = QLineEdit(self.cliente[3])
            layout.addWidget(self.label_telefono)
            layout.addWidget(self.input_telefono)

            # Botones
            botones_layout = QHBoxLayout()
            self.boton_guardar = QPushButton("Guardar")
            self.boton_guardar.clicked.connect(self.accept)
            self.boton_cancelar = QPushButton("Cancelar")
            self.boton_cancelar.clicked.connect(self.reject)
            botones_layout.addWidget(self.boton_guardar)
            botones_layout.addWidget(self.boton_cancelar)
            layout.addLayout(botones_layout)

            self.setLayout(layout)

        def obtener_datos(self):
            return {
                'nombre': self.input_nombre.text(),
                'mail': self.input_mail.text(),
                'telefono': self.input_telefono.text()
            }

    def volver_al_inicio(self):
        self.close()
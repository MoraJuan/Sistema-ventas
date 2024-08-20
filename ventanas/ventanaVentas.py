from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
from utils.database import conectar_db, crear_tabla_productos, mostrar_productos
from ventanas.ventanaCobro import VentanaCobro

class VentanaVentas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas")
        self.setGeometry(100, 100, 800, 600)

        self.productos = []

        self.crear_widgets()
        self.crear_layout()
        self.cargar_productos()  # Cargar productos desde la base de datos al iniciar

    def crear_widgets(self):
        # Widgets para agregar productos
        self.etiqueta_producto = QLabel("Producto:")
        self.entrada_producto = QLineEdit()
        self.etiqueta_precio = QLabel("Precio:")
        self.entrada_precio = QLineEdit()
        self.etiqueta_cantidad = QLabel("Cantidad:")
        self.entrada_cantidad = QLineEdit()
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.agregar_producto)
        self.boton_eliminar_seleccionado = QPushButton("Eliminar Producto Seleccionado")
        self.boton_eliminar_seleccionado.clicked.connect(self.eliminar_producto_seleccionado)

        # Tabla para mostrar los productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(4)
        self.tabla_productos.setHorizontalHeaderLabels(["ID", "Producto", "Precio", "Cantidad"])

        # Botones para finalizar la venta
        self.boton_finalizar = QPushButton("Volver al Inicio")
        self.boton_finalizar.clicked.connect(self.volver_al_inicio)

        # Aplicar estilos a los widgets
        self.aplicar_estilos()

    def crear_layout(self):
        layout_principal = QVBoxLayout()

        # Layout para agregar productos
        layout_agregar = QHBoxLayout()
        layout_agregar.addWidget(self.etiqueta_producto)
        layout_agregar.addWidget(self.entrada_producto)
        layout_agregar.addWidget(self.etiqueta_precio)
        layout_agregar.addWidget(self.entrada_precio)
        layout_agregar.addWidget(self.etiqueta_cantidad)
        layout_agregar.addWidget(self.entrada_cantidad)
        layout_agregar.addWidget(self.boton_agregar)
        layout_principal.addLayout(layout_agregar)

        # Agregamos la tabla de productos
        layout_principal.addWidget(self.tabla_productos)

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
        self.etiqueta_producto.setStyleSheet(estilo_etiqueta)
        self.etiqueta_precio.setStyleSheet(estilo_etiqueta)
        self.etiqueta_cantidad.setStyleSheet(estilo_etiqueta)

        # Estilos para las entradas de texto
        estilo_entrada = "padding: 5px; font-size: 14px;"
        self.entrada_producto.setStyleSheet(estilo_entrada)
        self.entrada_precio.setStyleSheet(estilo_entrada)
        self.entrada_cantidad.setStyleSheet(estilo_entrada)

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
        self.tabla_productos.setStyleSheet(estilo_tabla)

    def agregar_producto(self):
        producto = self.entrada_producto.text()
        precio = self.entrada_precio.text()
        cantidad = self.entrada_cantidad.text()

        if producto and precio and cantidad:
            try:
                precio = float(precio)
                cantidad = int(cantidad)

                # Insertar el producto en la base de datos
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)", (producto, precio, cantidad))
                conn.commit()

                # Obtener el ID del producto recién insertado
                cursor.execute("SELECT last_insert_rowid()")
                producto_id = cursor.fetchone()[0]
                conn.close()

                self.productos.append((producto_id, producto, precio, cantidad))
                self.actualizar_tabla()
                self.entrada_producto.clear()
                self.entrada_precio.clear()
                self.entrada_cantidad.clear()
            except ValueError:
                QMessageBox.warning(self, "Error", "El precio y la cantidad deben ser números.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingresa el producto, el precio y la cantidad.")

    def actualizar_tabla(self):
        self.tabla_productos.setRowCount(len(self.productos))
        for fila, (producto_id, producto, precio, cantidad) in enumerate(self.productos):
            self.tabla_productos.setItem(fila, 0, QTableWidgetItem(str(producto_id)))
            self.tabla_productos.setItem(fila, 1, QTableWidgetItem(producto))
            self.tabla_productos.setItem(fila, 2, QTableWidgetItem(str(precio)))
            self.tabla_productos.setItem(fila, 3, QTableWidgetItem(str(cantidad)))

    def cargar_productos(self):
        productos_db = mostrar_productos()
        self.productos = [(producto[0], producto[1], producto[2], producto[3]) for producto in productos_db]
        self.actualizar_tabla()

    def eliminar_producto_seleccionado(self):
        fila_seleccionada = self.tabla_productos.currentRow()
        if fila_seleccionada != -1:
            producto = self.productos.pop(fila_seleccionada)
            self.actualizar_tabla()

            # Eliminar el producto seleccionado de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto[0],))
            conn.commit()
            conn.close()
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un producto para eliminar.")

    def volver_al_inicio(self):
        self.close()
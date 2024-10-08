from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QHeaderView
)
from PyQt5.QtWidgets import QWidget
from controladores.ventana_controller import calcular_total
from utils.producto import buscar_producto, buscar_producto_por_nombre_bd
from models.producto import Producto


class VentanaCobro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas")
        self.showMaximized()

        self.productos = []
        self.carrito = []
        self.cantidad_total = 0 
        self.suma_total = 0

        self.crear_widgets()
        self.crear_layout()

    def cargar_productos(self, productos):
        self.productos = [Producto(nombre, precio, cantidad) for nombre, precio, cantidad in productos]
        self.actualizar_tabla()

    def crear_widgets(self):
        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(3)
        self.tabla_productos.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad"])
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Búsqueda de producto por ID
        self.label_buscar_producto = QLabel("Buscar Producto por ID:")
        self.entrada_buscar_producto = QLineEdit()
        self.boton_buscar_producto = QPushButton("Buscar por ID")
        self.boton_buscar_producto.clicked.connect(self.buscar_producto_por_id)

        # Búsqueda de producto por nombre
        self.label_buscar_nombre = QLabel("Buscar Producto por Nombre:")
        self.entrada_buscar_nombre = QLineEdit()
        self.boton_buscar_nombre = QPushButton("Buscar por Nombre")
        self.boton_buscar_nombre.clicked.connect(self.buscar_producto_por_nombre)

        #Suma total
        self.label_suma_total = QLabel("Suma Total: $0.00")

        # Botones de acción
        self.boton_finalizar = QPushButton("Finalizar Venta")
        self.boton_finalizar.clicked.connect(self.finalizar_venta)
        self.boton_cancelar = QPushButton("Cancelar Venta")
        self.boton_cancelar.clicked.connect(self.cancelar_venta)
        self.boton_agregar_carrito = QPushButton("Agregar al Carrito")
        #self.boton_agregar_carrito.clicked.connect(self.agregar_al_carrito)
        self.boton_limpiar_carrito = QPushButton("Limpiar Carrito")
        self.boton_limpiar_carrito.clicked.connect(self.limpiar_carrito)
        self.boton_generar_factura = QPushButton("Generar Factura")
        self.boton_generar_factura.clicked.connect(self.generar_factura)
        #Boton para salir
        self.boton_salir = QPushButton("Volver al Inicio")
        self.boton_salir.clicked.connect(self.volver_al_inicio)

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
        self.boton_buscar_nombre.setStyleSheet(estilo_boton)
        self.boton_generar_factura.setStyleSheet(estilo_boton)
        self.boton_salir.setStyleSheet(estilo_boton)

    def crear_layout(self):
        layout_principal = QVBoxLayout()

        # Sección de búsqueda por ID
        layout_buscar_id = QHBoxLayout()
        layout_buscar_id.addWidget(self.label_buscar_producto)
        layout_buscar_id.addWidget(self.entrada_buscar_producto)
        layout_buscar_id.addWidget(self.boton_buscar_producto)
        layout_principal.addLayout(layout_buscar_id)

        # Sección de búsqueda por nombre
        layout_buscar_nombre = QHBoxLayout()
        layout_buscar_nombre.addWidget(self.label_buscar_nombre)
        layout_buscar_nombre.addWidget(self.entrada_buscar_nombre)
        layout_buscar_nombre.addWidget(self.boton_buscar_nombre)
        layout_principal.addLayout(layout_buscar_nombre)

        # Tabla de productos
        layout_principal.addWidget(self.tabla_productos)
        #Apartado suma total 
        layout_suma_total = QHBoxLayout()
        layout_suma_total.addStretch(1)  # Espacio flexible
        layout_suma_total.addWidget(self.label_suma_total)
        layout_principal.addLayout(layout_suma_total)

        # Botones de acción
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_finalizar)
        layout_botones.addWidget(self.boton_cancelar)
        layout_botones.addStretch(1)  # Espacio flexible
        layout_botones.addWidget(self.boton_agregar_carrito)
        layout_botones.addWidget(self.boton_limpiar_carrito)
        layout_botones.addWidget(self.boton_generar_factura)
        layout_botones.addWidget(self.boton_salir)
        layout_principal.addLayout(layout_botones)
        

        widget_central = QWidget()
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

    def actualizar_tabla(self):
        # Usamos solo los productos en el carrito para evitar duplicados
        self.tabla_productos.setRowCount(len(self.carrito))
        cantidad_cobro = 1
        
        # Llenamos la tabla con los productos del carrito
        

        for fila, producto in enumerate(self.carrito):
            if isinstance(producto, Producto):
                self.tabla_productos.setItem(fila, 0, QTableWidgetItem(producto.nombre))
                self.tabla_productos.setItem(fila, 1, QTableWidgetItem(str(producto.precio)))
                self.tabla_productos.setItem(fila, 2, QTableWidgetItem(str(cantidad_cobro)))
                self.suma_total += producto.precio * float(cantidad_cobro)
        self.label_suma_total.setText(f"Suma Total: ${self.suma_total:.2f}")

    def buscar_producto_por_nombre(self):
        nombre = self.entrada_buscar_nombre.text()
        if not nombre:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un nombre de producto.")
            return

        productos = buscar_producto_por_nombre_bd(nombre)
        if productos:
            nuevos_productos = [Producto(producto[1], producto[2], producto[3]) for producto in productos]
            for nuevo_producto in nuevos_productos:
                if nuevo_producto not in self.carrito:
                    self.carrito.append(nuevo_producto)
                    #funcion para que carrito le disminuya la cantidad de productos
                    nuevo_producto.disminuir_cantidad(1)
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "Producto no encontrado.")

    def buscar_producto_por_id(self):
        id_text = self.entrada_buscar_producto.text()
        if not id_text.isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingresa un ID válido.")
            return

        productos = buscar_producto(int(id_text))
        if productos:
            nuevos_productos = [Producto(producto[1], producto[2], producto[3]) for producto in productos]
            for nuevo_producto in nuevos_productos:
                if nuevo_producto not in self.carrito:
                    self.carrito.append(nuevo_producto)
                    self.cantidad_total += 1
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "Producto no encontrado.")
    #Esta funcion ya no se usa ya que en el buscar le hacemos el append directamente con el carrito
    #Hacia problema con la visualizacion de la tabla de productos
    '''def agregar_al_carrito(self):
        if self.productos:
            producto = self.productos[0]
            self.carrito.append(producto)
            self.ver_carrito()
            QMessageBox.information(self, "Carrito", "Producto agregado al carrito.")
        else:
            QMessageBox.warning(self, "Error", "No hay productos para agregar al carrito.")
    '''
    def limpiar_carrito(self):
        self.carrito = []
        QMessageBox.information(self, "Carrito", "Carrito limpiado.")

    def finalizar_venta(self):
        if self.carrito:
            total = self.suma_total
            QMessageBox.information(self, "Venta Finalizada", f"Total a pagar: {total}")
            self.suma_total = 0
            self.generar_factura()
            self.carrito = []
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")

    def cancelar_venta(self):
        if self.productos or self.carrito:
            self.productos = []
            self.carrito = []
            self.actualizar_tabla()
            QMessageBox.information(self, "Venta Cancelada", "La venta ha sido cancelada.")
        else:
            QMessageBox.warning(self, "Error", "No hay productos o carrito para cancelar.")

    def generar_factura(self):
        if not self.carrito:
            QMessageBox.warning(self, "Error", "No hay productos en el carrito para generar una factura.")
            return

        total = calcular_total(self.carrito)
        factura_texto = "Factura de Venta\n"
        factura_texto += "================\n"
        for producto in self.carrito:
            factura_texto += f"Producto: {producto.nombre}\n"
            factura_texto += f"Precio: ${producto.precio:.2f}\n"
            factura_texto += f"Cantidad: {producto.cantidad}\n"
            factura_texto += "----------------\n"
        factura_texto += f"Total: ${total:.2f}\n"

        # Guardar la factura en un archivo de texto
        with open("factura.txt", "w") as archivo:
            archivo.write(factura_texto)

        QMessageBox.information(self, "Factura Generada", "La factura ha sido generada y guardada como 'factura.txt'.")

    def ver_carrito(self):
        carrito_texto = "Carrito de Compras\n"
        carrito_texto += "=================\n"
        for producto in self.carrito:
            carrito_texto += f"Producto: {producto.nombre}\n"
            carrito_texto += f"Precio: ${producto.precio:.2f}\n"

        QMessageBox.information(self, "Carrito de Compras", carrito_texto)



    def volver_al_inicio(self):
        self.close()

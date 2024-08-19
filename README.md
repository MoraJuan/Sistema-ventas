Sistema de Ventas
  Descripción del Proyecto
  El Sistema de Ventas es una aplicación de escritorio desarrollada en Python utilizando el framework PyQt5. Este sistema permite gestionar productos, realizar ventas y llevar un control de inventario de manera eficiente. La aplicación está diseñada para ser intuitiva y fácil de usar, proporcionando una interfaz gráfica amigable para los usuarios.
  
Funcionalidades
  Ventana Principal
  Agregar Producto / Eliminar Producto: Permite agregar nuevos productos al inventario o eliminar productos existentes.
  Realizar Cobro: Inicia el proceso de cobro para los productos seleccionados.
  Estado: Muestra el estado actual del sistema.
  Ventana de Ventas
  Agregar Producto: Permite ingresar detalles de un nuevo producto (nombre, precio, cantidad) y agregarlo al inventario.
  Eliminar Producto Seleccionado: Elimina el producto seleccionado de la lista.
  Tabla de Productos: Muestra todos los productos disponibles en el inventario con sus respectivos detalles.
  Volver al Inicio: Regresa a la ventana principal.
  Ventana de Cobro
  Buscar Producto por ID: Permite buscar un producto específico por su ID.
  Agregar al Carrito: Agrega los productos seleccionados al carrito de compras.
  Limpiar Carrito: Vacía el carrito de compras.
  Finalizar Venta: Calcula el total de la venta y finaliza el proceso de cobro.
  Cancelar Venta: Cancela la venta actual y limpia el carrito.
Tecnologías Utilizadas
  Python: Lenguaje de programación principal utilizado para desarrollar la lógica del sistema.
  PyQt5: Framework utilizado para crear la interfaz gráfica de usuario (GUI).
  SQLite: Base de datos ligera utilizada para almacenar la información de los productos.
  QMessageBox: Utilizado para mostrar mensajes de alerta e información al usuario.
  QTableWidget: Utilizado para mostrar tablas de datos en la interfaz gráfica.
Estructura del Proyecto
  main.py: Archivo principal que inicia la aplicación.
  ventanas/: Directorio que contiene las diferentes ventanas de la aplicación.
  ventana_principal.py: Contiene la lógica y la interfaz de la ventana principal.
  ventanaVentas.py: Contiene la lógica y la interfaz de la ventana de ventas.
  ventanaCobro.py: Contiene la lógica y la interfaz de la ventana de cobro.
  controladores/: Directorio que contiene los controladores de la aplicación.
  ventana_controller.py: Contiene funciones auxiliares para el cálculo de totales y otras operaciones.
  utils/: Directorio que contiene utilidades y funciones auxiliares.
  database.py: Contiene funciones para interactuar con la base de datos SQLite.

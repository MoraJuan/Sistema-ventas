from PyQt5.QtWidgets import QTableWidget

class TablaProductos(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Personalizaciones adicionales de la tabla, si es necesario
import sys
from PyQt5.QtWidgets import QApplication
from ventanas.ventana_principal import VentanaVentas, VentanaPrincipal
from ventanas.landing.ventana_inicio import VentanaInicio

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    sys.exit((app.exec_()))
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

# Crear una aplicación Qt
app = QApplication([])

# Crear una ventana principal
window = QMainWindow()
window.setWindowTitle("Mi Aplicación")

# Crear un widget Label
label = QLabel("Hola, PyQt!")
window.setCentralWidget(label)

# Mostrar la ventana
window.show()

# Ejecutar el bucle principal de la interfaz
app.exec_()

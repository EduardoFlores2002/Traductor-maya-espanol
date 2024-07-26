from src.gui import MayaToSpanishTranslator
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = MayaToSpanishTranslator()
    translator.show()
    sys.exit(app.exec_())


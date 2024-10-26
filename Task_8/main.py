import sys
from PyQt5.QtWidgets import QApplication
from gui import SimulationApp

if __name__ == "__main__":
    """
    Основной блок для запуска приложения PyQt5.
    """
    app = QApplication(sys.argv)
    window = SimulationApp()
    window.show()
    sys.exit(app.exec_())

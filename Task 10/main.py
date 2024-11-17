import sys
from PyQt5.QtWidgets import QApplication
from gui import ChargeFieldSimulator
from calculations import plot_field


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChargeFieldSimulator(plot_callback=plot_field)
    window.show()
    sys.exit(app.exec_())

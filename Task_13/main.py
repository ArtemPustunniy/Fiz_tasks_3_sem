import sys
from PyQt5.QtWidgets import QApplication
from gui import ChargeFieldSimulator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChargeFieldSimulator()
    window.show()
    sys.exit(app.exec_())

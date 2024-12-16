import sys
from PyQt5.QtWidgets import QApplication
from gui import DielectricFieldSimulator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DielectricFieldSimulator()
    window.show()
    sys.exit(app.exec_())

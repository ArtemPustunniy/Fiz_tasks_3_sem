import sys
from PyQt5.QtWidgets import QApplication
from UserInterface import BallisticMotionApp

g = 9.81


app = QApplication(sys.argv)
ex = BallisticMotionApp()
ex.show()
sys.exit(app.exec_())


# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui import ProjectileApp  # Import the ProjectileApp class

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectileApp()  # Create an instance of the application
    ex.show()  # Show the application window
    sys.exit(app.exec_())  # Start the application event loop



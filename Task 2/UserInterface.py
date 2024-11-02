from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Utils import *


class BallisticMotionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Баллистическое движение')
        self.setGeometry(750, 350, 400, 200)

        layout = QVBoxLayout()

        # Height input
        self.label_h = QLabel('Введите высоту (h > 0):')
        self.input_h = QLineEdit()
        layout.addWidget(self.label_h)
        layout.addWidget(self.input_h)

        # Initial velocity input
        self.label_v0 = QLabel('Введите начальную скорость (м/с):')
        self.input_v0 = QLineEdit()
        layout.addWidget(self.label_v0)
        layout.addWidget(self.input_v0)

        # Angle input
        self.label_angle = QLabel('Введите угол броска (градусы):')
        self.input_angle = QLineEdit()
        layout.addWidget(self.label_angle)
        layout.addWidget(self.input_angle)

        # Button to plot graphs
        self.plot_button = QPushButton('Построить графики')
        self.plot_button.clicked.connect(self.on_plot_button_clicked)
        layout.addWidget(self.plot_button)

        # Set layout
        self.setLayout(layout)

        # Apply new dark theme style
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
            }
            QLabel {
                font-size: 14px;
                color: #ffffff;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #5b5b5b;
                border-radius: 10px;
                background-color: #444444;
                color: #ffffff;
            }
            QPushButton {
                font-size: 14px;
                background-color: #ff6f61;
                color: #ffffff;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #ff6f61;
            }
            QPushButton:hover {
                background-color: #ff5f50;
                border-color: #ff5f50;
            }
            QPushButton:pressed {
                background-color: #ff4f40;
                border-color: #ff4f40;
            }
        """)

    def on_plot_button_clicked(self):
        try:
            h = float(self.input_h.text())
            v0 = float(self.input_v0.text())
            angle_deg = float(self.input_angle.text())

            if h < 0 or v0 < 0:
                raise ValueError

            # Calculate motion
            t, x, y, v, vx, vy = ballistic_motion(h, v0, angle_deg)

            # Plot graphs
            plot_trajectory(x, y)

            plot_velocity(t, v)
            plot_coordinates(t, x, y)

        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректные з

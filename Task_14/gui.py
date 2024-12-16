from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QDesktopWidget,
    QMessageBox,
)
from PyQt5.QtGui import QFont
from calculations import calculate_refraction, generate_plot


class DielectricFieldSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Преломление электрического поля")
        self.resize(600, 400)
        self.center_window()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.header_label = QLabel("Параметры границы диэлектриков")
        self.header_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header_label)

        self.epsilon1_input = self.create_input_field(
            "Диэлектрическая проницаемость первой среды (ε1):"
        )
        self.epsilon2_input = self.create_input_field(
            "Диэлектрическая проницаемость второй среды (ε2):"
        )
        self.angle_input = self.create_input_field("Угол падения (в градусах):")
        self.e0_input = self.create_input_field("Модуль напряжённости (E0):")

        self.simulate_button = QPushButton("Построить график")
        self.simulate_button.setStyleSheet(
            "background-color: #006400; color: white; font-size: 14px;"
        )
        self.simulate_button.clicked.connect(self.validate_and_simulate)
        layout.addWidget(self.simulate_button)

        self.setStyleSheet("background-color: #f7f7f7;")

    def create_input_field(self, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12))
        input_field = QLineEdit()
        input_field.setPlaceholderText("Введите значение")
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.centralWidget().layout().addLayout(layout)
        return input_field

    def center_window(self):
        screen_geometry = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry)
        self.move(frame_geometry.topLeft())

    def validate_and_simulate(self):
        try:
            epsilon1 = float(self.epsilon1_input.text())
            epsilon2 = float(self.epsilon2_input.text())
            angle = float(self.angle_input.text())
            e0 = float(self.e0_input.text())

            if epsilon1 <= 0 or epsilon2 <= 0 or not (0 <= angle <= 90) or e0 <= 0:
                raise ValueError("Проверьте корректность входных данных!")

            generate_plot(epsilon1, epsilon2, angle, e0)

        except ValueError as e:
            QMessageBox.critical(self, "Ошибка ввода", str(e))

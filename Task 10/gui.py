from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QGridLayout, QMessageBox, QDesktopWidget
)
from PyQt5.QtGui import QFont


class ChargeFieldSimulator(QMainWindow):
    def __init__(self, plot_callback):
        super().__init__()
        self.setWindowTitle("Электростатическое поле")
        self.resize(800, 600)
        self.plot_callback = plot_callback

        self.center_window()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.header_label = QLabel("Ввод данных")
        self.header_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.header_label.setStyleSheet("color: #006400;")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        self.num_charges_label = QLabel("Количество зарядов:")
        self.num_charges_input = QLineEdit()
        self.num_charges_input.setPlaceholderText("Введите число")

        self.add_charges_button = QPushButton("Создать поля")
        self.add_charges_button.setStyleSheet("background-color: #006400; color: white;")
        self.add_charges_button.clicked.connect(self.create_charge_inputs)

        num_charges_layout = QHBoxLayout()
        num_charges_layout.addWidget(self.num_charges_label)
        num_charges_layout.addWidget(self.num_charges_input)
        num_charges_layout.addWidget(self.add_charges_button)

        self.layout.addLayout(num_charges_layout)

        self.charges_layout = QGridLayout()
        self.layout.addLayout(self.charges_layout)

        self.simulate_button = QPushButton("Запустить симуляцию")
        self.simulate_button.setStyleSheet("background-color: #006400; color: white; font-size: 14px;")
        self.simulate_button.clicked.connect(self.validate_and_simulate)
        self.layout.addWidget(self.simulate_button)

        self.charge_entries = []

        self.setStyleSheet("background-color: #f7f7f7;")

    def center_window(self):
        screen_geometry = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry)
        self.move(frame_geometry.topLeft())

    def create_charge_inputs(self):
        try:
            num_charges = int(self.num_charges_input.text())
            if num_charges <= 0:
                raise ValueError("Количество зарядов должно быть положительным числом.")

            for i in reversed(range(self.charges_layout.count())):
                widget = self.charges_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.charge_entries = []

            for i in range(num_charges):
                label = QLabel(f"Заряд {i + 1}:")
                x_input = QLineEdit()
                x_input.setPlaceholderText("x (-5 до 5)")

                y_input = QLineEdit()
                y_input.setPlaceholderText("y (-5 до 5)")

                q_input = QLineEdit()
                q_input.setPlaceholderText("q (заряд)")

                color_input = QLineEdit()
                color_input.setPlaceholderText("Цвет (red, green, blue, yellow)")

                label.setFont(QFont("Arial", 12))
                self.charges_layout.addWidget(label, i, 0)
                self.charges_layout.addWidget(QLabel("x:"), i, 1)
                self.charges_layout.addWidget(x_input, i, 2)
                self.charges_layout.addWidget(QLabel("y:"), i, 3)
                self.charges_layout.addWidget(y_input, i, 4)
                self.charges_layout.addWidget(QLabel("q:"), i, 5)
                self.charges_layout.addWidget(q_input, i, 6)
                self.charges_layout.addWidget(QLabel("Цвет:"), i, 7)
                self.charges_layout.addWidget(color_input, i, 8)

                self.charge_entries.append({"x": x_input, "y": y_input, "q": q_input, "color": color_input})
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def validate_and_simulate(self):
        charges = []
        allowed_colors = {"red", "green", "blue", "yellow"}
        try:
            for i, entry in enumerate(self.charge_entries):
                x = float(entry["x"].text())
                y = float(entry["y"].text())
                q = float(entry["q"].text())
                color = entry["color"].text().strip().lower()

                if color not in allowed_colors:
                    raise ValueError(f"Цвет заряда {i + 1} должен быть red, green, blue или yellow.")

                if not (-5 <= x <= 5 and -5 <= y <= 5):
                    raise ValueError(f"Координаты заряда {i + 1} должны быть в пределах от -5 до 5.")

                charges.append({"q": q, "pos": (x, y), "color": color})

            self.plot_callback(charges)
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

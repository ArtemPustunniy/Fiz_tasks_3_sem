import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QMessageBox,
    QDesktopWidget,
)
from PyQt5.QtGui import QFont
from calculations import calculate_field, calculate_dipole_effect
import matplotlib.pyplot as plt


class ChargeFieldSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Электростатическое поле")
        self.resize(800, 600)

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
        self.add_charges_button.setStyleSheet(
            "background-color: #006400; color: white;"
        )
        self.add_charges_button.clicked.connect(self.create_charge_inputs)

        num_charges_layout = QHBoxLayout()
        num_charges_layout.addWidget(self.num_charges_label)
        num_charges_layout.addWidget(self.num_charges_input)
        num_charges_layout.addWidget(self.add_charges_button)

        self.layout.addLayout(num_charges_layout)

        self.charges_layout = QGridLayout()
        self.layout.addLayout(self.charges_layout)

        self.dipole_label = QLabel("Параметры диполя:")
        self.dipole_label.setFont(QFont("Arial", 12))
        self.dipole_layout = QHBoxLayout()

        self.dipole_x_input = QLineEdit()
        self.dipole_x_input.setPlaceholderText("x (позиция диполя)")

        self.dipole_y_input = QLineEdit()
        self.dipole_y_input.setPlaceholderText("y (позиция диполя)")

        self.dipole_px_input = QLineEdit()
        self.dipole_px_input.setPlaceholderText("px (момент по x)")

        self.dipole_py_input = QLineEdit()
        self.dipole_py_input.setPlaceholderText("py (момент по y)")

        self.dipole_layout.addWidget(self.dipole_label)
        self.dipole_layout.addWidget(self.dipole_x_input)
        self.dipole_layout.addWidget(self.dipole_y_input)
        self.dipole_layout.addWidget(self.dipole_px_input)
        self.dipole_layout.addWidget(self.dipole_py_input)

        self.layout.addLayout(self.dipole_layout)

        self.simulate_button = QPushButton("Запустить симуляцию")
        self.simulate_button.setStyleSheet(
            "background-color: #006400; color: white; font-size: 14px;"
        )
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

                label.setFont(QFont("Arial", 12))
                self.charges_layout.addWidget(label, i, 0)
                self.charges_layout.addWidget(QLabel("x:"), i, 1)
                self.charges_layout.addWidget(x_input, i, 2)
                self.charges_layout.addWidget(QLabel("y:"), i, 3)
                self.charges_layout.addWidget(y_input, i, 4)
                self.charges_layout.addWidget(QLabel("q:"), i, 5)
                self.charges_layout.addWidget(q_input, i, 6)

                self.charge_entries.append({"x": x_input, "y": y_input, "q": q_input})
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def validate_and_simulate(self):
        charges = []
        has_error = False

        for i, entry in enumerate(self.charge_entries):
            try:
                x = entry["x"].text().strip()
                y = entry["y"].text().strip()
                q = entry["q"].text().strip()

                if not x or not y or not q:
                    raise ValueError(
                        f"Все поля для заряда {i + 1} должны быть заполнены."
                    )

                x = float(x)
                y = float(y)
                q = float(q)

                if not (-5 <= x <= 5 and -5 <= y <= 5):
                    raise ValueError(
                        f"Координаты заряда {i + 1} должны быть в пределах от -5 до 5."
                    )

                charges.append({"q": q, "pos": (x, y)})
            except ValueError as e:
                if not has_error:
                    QMessageBox.critical(self, "Ошибка", str(e))
                    has_error = True
                break

        if not has_error:
            try:
                dipole_x = float(self.dipole_x_input.text().strip())
                dipole_y = float(self.dipole_y_input.text().strip())
                dipole_px = float(self.dipole_px_input.text().strip())
                dipole_py = float(self.dipole_py_input.text().strip())
                dipole = {"pos": (dipole_x, dipole_y), "moment": (dipole_px, dipole_py)}
            except ValueError:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Все поля для диполя должны быть заполнены и корректны.",
                )
                return

            self.plot_field(charges, dipole)

    def plot_field(self, charges, dipole):
        x = np.linspace(-5, 5, 300)
        y = np.linspace(-5, 5, 300)
        X, Y = np.meshgrid(x, y)

        Ex, Ey, V = calculate_field(X, Y, charges)

        force_x, force_y, torque = calculate_dipole_effect(X, Y, Ex, Ey, dipole)

        plt.figure(figsize=(10, 8))
        plt.streamplot(
            X,
            Y,
            Ex,
            Ey,
            color=np.log(np.sqrt(Ex**2 + Ey**2) + 1),
            linewidth=1.5,
            cmap="hsv",
            density=2.0,
        )
        plt.contour(X, Y, V, levels=50, cmap="coolwarm", alpha=0.7)
        plt.colorbar(label="Магнитуда электрического поля (логарифм)")

        for charge in charges:
            x0, y0 = charge["pos"]
            plt.scatter(x0, y0, color="red", s=200, edgecolor="black")

        plt.quiver(
            dipole["pos"][0],
            dipole["pos"][1],
            force_x,
            force_y,
            color="blue",
            scale=10,
            label="Сила на диполь",
        )
        plt.title(f"Электростатическое поле и диполь\\nМомент силы: {torque:.2e}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid()
        plt.show()
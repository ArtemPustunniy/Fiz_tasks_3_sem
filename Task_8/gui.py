from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QApplication,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from physics import plot_energy_transformations


class SimulationApp(QWidget):
    """
    GUI приложение для ввода параметров осциллятора и запуска симуляции.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Симуляция колебаний")
        self.resize(400, 400)
        self.center_window()

        self.title = QLabel("Ввод данных", self)
        self.title.setFont(QFont("Arial", 16))
        self.title.setStyleSheet("color: green")

        self.mass_label = QLabel("Масса (кг):", self)
        self.mass_input = QLineEdit(self)

        self.spring_label = QLabel("Коэффициент жесткости (Н/м):", self)
        self.spring_input = QLineEdit(self)

        self.damping_label = QLabel("Коэффициент сопротивления (Н·с/м):", self)
        self.damping_input = QLineEdit(self)

        self.displacement_label = QLabel("Начальное смещение (м):", self)
        self.displacement_input = QLineEdit(self)

        self.velocity_label = QLabel("Начальная скорость (м/с):", self)
        self.velocity_input = QLineEdit(self)

        self.time_label = QLabel("Время моделирования (с):", self)
        self.time_input = QLineEdit(self)

        self.start_button = QPushButton("Запустить симуляцию", self)
        self.start_button.setStyleSheet("background-color: green; color: white")
        self.start_button.clicked.connect(self.run_simulation)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.mass_label)
        layout.addWidget(self.mass_input)
        layout.addWidget(self.spring_label)
        layout.addWidget(self.spring_input)
        layout.addWidget(self.damping_label)
        layout.addWidget(self.damping_input)
        layout.addWidget(self.displacement_label)
        layout.addWidget(self.displacement_input)
        layout.addWidget(self.velocity_label)
        layout.addWidget(self.velocity_input)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def center_window(self):
        """
        Центрирование окна приложения по центру экрана.
        """
        screen_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().screenGeometry().center()
        screen_geometry.moveCenter(screen_center)
        self.move(screen_geometry.topLeft())

    def run_simulation(self):
        """
        Запуск симуляции на основе введенных пользователем данных.
        """
        try:
            m = float(self.mass_input.text())
            k = float(self.spring_input.text())
            c = float(self.damping_input.text())
            x0 = float(self.displacement_input.text())
            v0 = float(self.velocity_input.text())
            t_end = float(self.time_input.text())
            plot_energy_transformations(m, k, c, x0, v0, t_end)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Пожалуйста, введите корректные числовые значения."
            )

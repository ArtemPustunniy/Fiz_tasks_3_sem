import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QFont


class CapacitorCalculator(QWidget):
    """
    Класс для расчета параметров плоского конденсатора с использованием графического интерфейса.
    """

    def __init__(self):
        """
        Инициализация класса, создание графического интерфейса.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Создает элементы интерфейса приложения.
        """
        self.setWindowTitle("Расчет параметров конденсатора")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        header = QLabel("Ввод данных")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(header)

        input_grid = QGridLayout()

        input_grid.addWidget(QLabel("Напряжение (В):"), 0, 0)
        self.voltage_input = QLineEdit()
        input_grid.addWidget(self.voltage_input, 0, 1)

        input_grid.addWidget(QLabel("Расстояние между пластинами (м):"), 1, 0)
        self.distance_input = QLineEdit()
        input_grid.addWidget(self.distance_input, 1, 1)

        input_grid.addWidget(QLabel("Диэлектрическая проницаемость:"), 2, 0)
        self.dielectric_input = QLineEdit()
        input_grid.addWidget(self.dielectric_input, 2, 1)

        input_grid.addWidget(QLabel("Площадь пластин (м²):"), 3, 0)
        self.area_input = QLineEdit()
        input_grid.addWidget(self.area_input, 3, 1)

        input_grid.addWidget(QLabel("Подключен к источнику питания:"), 4, 0)
        self.connection_input = QComboBox()
        self.connection_input.addItems(["Да", "Нет"])
        input_grid.addWidget(self.connection_input, 4, 1)

        main_layout.addLayout(input_grid)

        button_layout = QHBoxLayout()
        calculate_button = QPushButton("Рассчитать параметры")
        calculate_button.setStyleSheet("background-color: green; color: white;")
        calculate_button.clicked.connect(self.calculate_parameters)
        button_layout.addWidget(calculate_button)

        main_layout.addLayout(button_layout)

        self.results_label = QLabel("")
        self.results_label.setStyleSheet("border: 1px solid black; padding: 10px; background-color: #f9f9f9;")
        main_layout.addWidget(self.results_label)

        self.setLayout(main_layout)

    def calculate_parameters(self):
        """
        Выполняет расчет параметров конденсатора и выводит результаты.
        """
        try:
            voltage = float(self.voltage_input.text())
            distance = float(self.distance_input.text())
            dielectric_constant = float(self.dielectric_input.text())
            area = float(self.area_input.text())
            is_connected = self.connection_input.currentText() == "Да"

            if distance <= 0 or dielectric_constant <= 0 or area <= 0:
                raise ValueError("Расстояние, проницаемость и площадь должны быть положительными числами.")

            epsilon_0 = 8.85e-12
            electric_field = voltage / distance
            capacitance = dielectric_constant * epsilon_0 * area / distance

            if is_connected:
                charge = capacitance * voltage
            else:
                charge = capacitance * voltage

            results = (
                f"<b>Результаты расчета:</b><br>"
                f"Напряженность поля: {electric_field:.2e} В/м<br>"
                f"Емкость: {capacitance:.2e} Ф<br>"
                f"Заряд: {charge:.2e} Кл"
            )
            self.results_label.setText(results)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")


if __name__ == "__main__":
    """
    Точка входа в приложение. Создает экземпляр приложения и запускает графический интерфейс.
    """
    app = QApplication(sys.argv)
    window = CapacitorCalculator()
    window.show()
    sys.exit(app.exec_())

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def gravitational_potential(x, y, m, g):
    """
    Calculates the gravitational potential.

    Parameters:
    x (float) -- the x-coordinate.
    y (float) -- the y-coordinate.
    m (float) -- the mass of the object.
    g (float) -- the gravitational acceleration.

    Returns:
    float -- the gravitational potential.
    """
    return m * g * y


def spring_potential(x, y, k):
    """
    Calculates the elastic potential energy.

    Parameters:
    x (float) -- the x-coordinate.
    y (float) -- the y-coordinate.
    k (float) -- the spring constant.

    Returns:
    float -- the elastic potential energy.
    """
    return 0.5 * k * (x ** 2 + y ** 2)


def weight_potential(x, y, weight):
    """
    Calculates the potential energy due to weight.

    Parameters:
    x (float) -- the x-coordinate.
    y (float) -- the y-coordinate.
    weight (float) -- the weight force.

    Returns:
    float -- the potential energy due to weight.
    """
    return weight * y


def unknown_potential(x, y, A, B, alpha, beta):
    """
    Calculates the potential for an unknown force modeled as a power function of coordinates.

    Parameters:
    x (float) -- the x-coordinate.
    y (float) -- the y-coordinate.
    A (float) -- the coefficient for the x term.
    B (float) -- the coefficient for the y term.
    alpha (int) -- the exponent for the x term.
    beta (int) -- the exponent for the y term.

    Returns:
    float -- the potential energy of the unknown force.
    """
    return A * x ** alpha + B * y ** beta


class InitialWindow(QWidget):
    """
    The initial window of the application where the user selects the forces they want to use in the simulation.
    """
    def __init__(self):
        """Initializes the window and sets up the layout with checkboxes for selecting forces."""
        super().__init__()

        self.setWindowTitle("Выбор сил")

        self.main_layout = QVBoxLayout()

        # Add title label
        title_label = QLabel("Выберите силы, которые хотите использовать")
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: green;")
        self.main_layout.addWidget(title_label)

        # Checkboxes for force selection
        self.spring_checkbox = QCheckBox("Использовать упругую силу")
        self.gravity_checkbox = QCheckBox("Использовать гравитацию")
        self.weight_checkbox = QCheckBox("Использовать силу тяжести")
        self.unknown_checkbox = QCheckBox("Добавить неизвестные силы")

        checkbox_style = "color: green;"
        self.spring_checkbox.setStyleSheet(checkbox_style)
        self.gravity_checkbox.setStyleSheet(checkbox_style)
        self.weight_checkbox.setStyleSheet(checkbox_style)
        self.unknown_checkbox.setStyleSheet(checkbox_style)

        self.main_layout.addWidget(self.spring_checkbox)
        self.main_layout.addWidget(self.gravity_checkbox)
        self.main_layout.addWidget(self.weight_checkbox)
        self.main_layout.addWidget(self.unknown_checkbox)

        # Button to proceed to the next window
        self.next_button = QPushButton("Далее")
        self.next_button.setStyleSheet(
            "background-color: green; color: white; font-size: 14px; height: 30px;"
        )
        self.next_button.clicked.connect(self.next_window)
        self.main_layout.addWidget(self.next_button)

        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: white;")

        self.center()

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def next_window(self):
        """
        Collects the selected forces and opens the data input window.

        This method stores the selected forces (spring, gravity, weight, unknown)
        and opens a new window for inputting the corresponding parameters.
        """
        self.choices = []
        if self.spring_checkbox.isChecked():
            self.choices.append('spring')
        if self.gravity_checkbox.isChecked():
            self.choices.append('gravity')
        if self.weight_checkbox.isChecked():
            self.choices.append('weight')
        if self.unknown_checkbox.isChecked():
            self.choices.append('unknown')

        self.data_window = DataWindow(self.choices)
        self.data_window.show()
        self.close()


class DataWindow(QWidget):
    """
    The data input window for the user to provide parameters for the selected forces.
    """
    def __init__(self, choices):
        """
        Initializes the window and sets up input fields based on the selected forces.

        Parameters:
        choices (list) -- a list of selected forces (e.g., 'spring', 'gravity').
        """
        super().__init__()

        self.choices = choices
        self.unknown_forces = []

        self.setWindowTitle("Ввод данных для выбранных сил")
        self.main_layout = QVBoxLayout()

        # Create input fields based on selected forces
        if 'spring' in self.choices:
            self.spring_input = self.create_input_field("Коэффициент жесткости для упругой силы k:")
        if 'gravity' in self.choices:
            self.gravity_mass_input = self.create_input_field("Масса для гравитационного поля (m):")
            self.gravity_g_input = self.create_input_field("Ускорение свободного падения (g):")
        if 'weight' in self.choices:
            self.weight_input = self.create_input_field("Сила тяжести:")

        # Input for unknown forces
        if 'unknown' in self.choices:
            self.unknown_count_input = self.create_input_field("Сколько неизвестных сил добавить?")
            self.add_unknown_forces_button = QPushButton("Добавить неизвестные силы")
            self.add_unknown_forces_button.setStyleSheet(
                "background-color: green; color: white; font-size: 14px; height: 30px;"
            )
            self.add_unknown_forces_button.clicked.connect(self.add_unknown_forces)
            self.main_layout.addWidget(self.add_unknown_forces_button)

        # Button to run the simulation
        self.run_button = QPushButton("Запустить симуляцию")
        self.run_button.setStyleSheet(
            "background-color: green; color: white; font-size: 14px; height: 30px;"
        )
        self.run_button.clicked.connect(self.run_simulation)
        self.main_layout.addWidget(self.run_button)

        self.setLayout(self.main_layout)
        self.setStyleSheet("background-color: white;")

        self.center()

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_input_field(self, label_text):
        """
        Creates an input field with a label.

        Parameters:
        label_text (str) -- the text for the input field label.

        Returns:
        QLineEdit -- the created input field.
        """
        layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setFont(QFont('Arial', 12))
        label.setStyleSheet("color: green;")
        layout.addWidget(label)

        input_field = QLineEdit()
        input_field.setFixedWidth(200)
        input_field.setStyleSheet("border: 1px solid green; padding: 2px;")
        layout.addWidget(input_field)

        self.main_layout.addLayout(layout)

        return input_field

    def add_unknown_forces(self):
        """
        Adds input fields for the unknown forces based on the number specified by the user.
        """
        try:
            count = int(self.unknown_count_input.text())
            for i in range(count):
                A_input = self.create_input_field(f"Коэффициент A для неизвестной силы {i+1}:")
                B_input = self.create_input_field(f"Коэффициент B для неизвестной силы {i+1}:")
                alpha_input = self.create_input_field(f"Степень для x (alpha) для силы {i+1}:")
                beta_input = self.create_input_field(f"Степень для y (beta) для силы {i+1}:")
                self.unknown_forces.append((A_input, B_input, alpha_input, beta_input))

            self.add_unknown_forces_button.setEnabled(False)
        except ValueError:
            print("Введите корректное количество неизвестных сил.")

    def run_simulation(self):
        """
        Runs the simulation by collecting input values and calculating the potential.

        This method collects the input values from the fields, calculates the potential
        for the selected forces, and displays the results.
        """
        try:
            choices = []

            if 'spring' in self.choices:
                k = float(self.spring_input.text())
                choices.append(('spring', k))
            if 'gravity' in self.choices:
                m = float(self.gravity_mass_input.text())
                g = float(self.gravity_g_input.text())
                choices.append(('gravity', m, g))
            if 'weight' in self.choices:
                weight = float(self.weight_input.text())
                choices.append(('weight', weight))

            unknown_forces = []
            for A_input, B_input, alpha_input, beta_input in self.unknown_forces:
                A = float(A_input.text())
                B = float(B_input.text())
                alpha = int(alpha_input.text())
                beta = int(beta_input.text())
                unknown_forces.append((A, B, alpha, beta))

            self.calculate_potential(choices, unknown_forces)
        except ValueError:
            print("Ошибка: Введите корректные числовые значения.")

    def calculate_potential(self, choices, unknown_forces):
        """
        Calculates and visualizes the total potential field based on the selected forces.

        Parameters:
        choices (list) -- a list of selected forces and their parameters.
        unknown_forces (list) -- a list of unknown forces and their parameters.
        """
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        total_potential = np.zeros_like(X)

        for choice in choices:
            if choice[0] == 'spring':
                k = choice[1]
                total_potential += spring_potential(X, Y, k)
            elif choice[0] == 'gravity':
                m, g = choice[1], choice[2]
                total_potential += gravitational_potential(X, Y, m, g)
            elif choice[0] == 'weight':
                weight = choice[1]
                total_potential += weight_potential(X, Y, weight)

        for force in unknown_forces:
            A, B, alpha, beta = force
            total_potential += unknown_potential(X, Y, A, B, alpha, beta)

        plt.figure()
        cp = plt.contourf(X, Y, total_potential, cmap='plasma')
        plt.colorbar(cp)
        plt.title('Поле потенциальной энергии')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


def main():
    """
    The main entry point of the application.

    This function initializes the QApplication and opens the initial window for force selection.
    """
    app = QApplication(sys.argv)

    window = InitialWindow()
    window.setGeometry(300, 300, 400, 300)
    window.center()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QGridLayout, QDesktopWidget, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from physics_and_math import calculate_trajectory
from validation import validate_input  # Import validation of data
import matplotlib.pyplot as plt
import numpy as np


class ProjectileApp(QWidget):
    """
    Class representing the main application window for simulating projectile motion
    with air resistance.

    This class provides the user interface (UI) for inputting parameters such as
    initial velocity, angle, height, and air resistance coefficient, and simulates
    the trajectory of the projectile based on the entered data.

    Methods:
    ----------
    __init__ :
        Initializes the application window and sets up the user interface.

    initUI :
        Sets up the layout of the UI, including labels, input fields, and buttons.

    center :
        Centers the application window on the screen.

    run_simulation :
        Collects input data, validates it, and runs the simulation if the data is correct.

    show_error_dialog :
        Displays a modal dialog box showing the validation errors if incorrect data is entered.

    plot_trajectory :
        Displays a matplotlib plot showing the trajectory of the projectile and the velocity over time.
    """

    def __init__(self):
        """Initializes the main application window and sets up the UI layout."""
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for the application window.

        This method configures the title, dimensions, and layout of the window, and
        adds input fields for user parameters, a button to start the simulation, and
        a green header for data entry.
        """
        # Set up window title and geometry
        self.setWindowTitle("Motion simulation with resistance air")
        self.setGeometry(100, 100, 800, 600)

        # Center the window on the screen
        self.center()

        layout = QVBoxLayout()

        # Header style for data input
        title_label = QLabel('Ввод данных')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("color: green;")
        layout.addWidget(title_label)

        # Grid layout for data input fields
        grid = QGridLayout()

        # Labels and input fields for initial velocity, angle, height, and resistance coefficient
        labels_text = [
            'Начальная скорость (м/с):',
            'Угол между вектором и горизонтом (градусы):',
            'Начальная высота (м):',
            'Коэффициент сопротивления среды k:'
        ]
        self.inputs = []

        # Loop to create input fields and add them to the layout
        for i, label_text in enumerate(labels_text):
            label = QLabel(label_text)
            label.setFont(QFont('Arial', 10))
            grid.addWidget(label, i, 0)
            line_edit = QLineEdit(self)
            self.inputs.append(line_edit)
            grid.addWidget(line_edit, i, 1)

        layout.addLayout(grid)

        # Button to start the simulation
        self.simulate_button = QPushButton('Запустить симуляцию', self)
        self.simulate_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.simulate_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.simulate_button)

        self.setLayout(layout)

    def center(self):
        """
        Centers the application window on the user's screen.

        This method calculates the available geometry of the desktop screen and moves
        the window to be positioned at the center of the screen.
        """
        qr = self.frameGeometry()  # Get window's geometry
        cp = QDesktopWidget().availableGeometry().center()  # Get center of the screen
        qr.moveCenter(cp)  # Move window's center to the center of the screen
        self.move(qr.topLeft())  # Adjust top-left corner

    def run_simulation(self):
        """
        Starts the simulation by collecting input data, validating it, and running the calculations.

        This method fetches input values from the input fields, checks them for validity using
        the `validate_input` function, and displays an error dialog if necessary. If the input is valid,
        it calls the trajectory calculation function and plots the results.
        """
        try:
            # Fetch data from input fields
            v0 = float(self.inputs[0].text())
            theta = float(self.inputs[1].text())
            h0 = float(self.inputs[2].text())
            k = float(self.inputs[3].text())
        except ValueError:
            # Show error dialog if input data cannot be converted to float
            self.show_error_dialog(["Пожалуйста, введите числовые значения."])
            return

        # Validate the input using external validation function
        errors = validate_input(v0, theta, h0, k)
        if errors:
            # Show error dialog if validation fails
            self.show_error_dialog(errors)
            return

        # Calculate trajectory using physics and math functions
        x, y, t, vx, vy = calculate_trajectory(v0, theta, h0, k)

        # Plot the trajectory and velocity
        self.plot_trajectory(x, y, t, vx, vy)

    def show_error_dialog(self, errors):
        """
        Displays a modal error dialog with a list of validation errors.

        This method creates a QMessageBox to show the list of errors in the dialog,
        allowing the user to correct their input.

        Parameters:
        errors -- list of validation error messages to display
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Ошибка ввода")
        msg.setText("Обнаружены следующие ошибки:")
        msg.setInformativeText("\n".join(errors))

        # Add Ok button and style it green
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setStyleSheet("background-color: green; color: white; font-weight: bold;")

        msg.exec_()

    def plot_trajectory(self, x, y, t, vx, vy):
        """
        Displays the simulation results in a matplotlib plot.

        This method creates four subplots: one for the projectile's trajectory (position over time),
        one for its speed over time, and two for the coordinates (x and y) over time.

        Parameters:
        x -- list of x coordinates (horizontal distance)
        y -- list of y coordinates (height)
        t -- list of time points
        vx -- list of velocity components along the x-axis
        vy -- list of velocity components along the y-axis
        """
        plt.figure(figsize=(15, 10))

        # Plot trajectory
        plt.subplot(2, 2, 1)
        plt.plot(x, y)
        plt.title('Траектория движения тела')
        plt.xlabel('x (м)')
        plt.ylabel('y (м)')
        plt.grid(True, which='both', linestyle='--', linewidth=1)
        plt.minorticks_on()

        # Plot velocity over time
        plt.subplot(2, 2, 2)
        plt.plot(t, np.sqrt(np.array(vx) ** 2 + np.array(vy) ** 2))
        plt.title('Зависимость скорости от времени')
        plt.xlabel('Время (с)')
        plt.ylabel('Скорость (м/с)')
        plt.grid(True, which='both', linestyle='--', linewidth=1)
        plt.minorticks_on()

        # Plot x-coordinate over time
        plt.subplot(2, 2, 3)
        plt.plot(t, x)
        plt.title('Зависимость координаты x от времени')
        plt.xlabel('Время (с)')
        plt.ylabel('x (м)')
        plt.grid(True, which='both', linestyle='--', linewidth=1)
        plt.minorticks_on()

        # Plot y-coordinate over time
        plt.subplot(2, 2, 4)
        plt.plot(t, y)
        plt.title('Зависимость координаты y от времени')
        plt.xlabel('Время (с)')
        plt.ylabel('y (м)')
        plt.grid(True, which='both', linestyle='--', linewidth=1)
        plt.minorticks_on()

        plt.tight_layout()

        # Show the plot in full screen
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()

        plt.show()


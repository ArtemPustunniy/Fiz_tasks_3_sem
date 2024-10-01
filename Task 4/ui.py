from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from logic import Body, collision_with_wall, elastic_collision


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel('Ввод данных')
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        title_label.setAlignment(Qt.AlignTop)
        title_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title_label)

        grid_layout = QGridLayout()

        self.width_input = self.create_input_row(grid_layout, 'Ширина оболочки (м):', 0, 0)
        self.height_input = self.create_input_row(grid_layout, 'Высота оболочки (м):', 1, 0)
        self.mass1_input = self.create_input_row(grid_layout, 'Масса тела 1 (кг):', 2, 0)
        self.velocity1_x_input = self.create_input_row(grid_layout, 'Скорость тела 1 по X (м/с):', 3, 0)
        self.velocity1_y_input = self.create_input_row(grid_layout, 'Скорость тела 1 по Y (м/с):', 4, 0)
        self.x1_input = self.create_input_row(grid_layout, 'Позиция тела 1 по X:', 5, 0)
        self.y1_input = self.create_input_row(grid_layout, 'Позиция тела 1 по Y:', 6, 0)

        self.mass2_input = self.create_input_row(grid_layout, 'Масса тела 2 (кг):', 2, 1)
        self.velocity2_x_input = self.create_input_row(grid_layout, 'Скорость тела 2 по X (м/с):', 3, 1)
        self.velocity2_y_input = self.create_input_row(grid_layout, 'Скорость тела 2 по Y (м/с):', 4, 1)
        self.x2_input = self.create_input_row(grid_layout, 'Позиция тела 2 по X:', 5, 1)
        self.y2_input = self.create_input_row(grid_layout, 'Позиция тела 2 по Y:', 6, 1)

        layout.addLayout(grid_layout)

        start_button = QPushButton('Запустить симуляцию')
        start_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        start_button.clicked.connect(self.start_simulation)
        layout.addWidget(start_button)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def create_input_row(self, layout, label_text, row, column, center=False):
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 14px;")
        input_field = QLineEdit()
        if center:
            layout.addWidget(label, row, column * 2, alignment=Qt.AlignCenter)
            layout.addWidget(input_field, row, column * 2 + 1, alignment=Qt.AlignCenter)
        else:
            layout.addWidget(label, row, column * 2)
            layout.addWidget(input_field, row, column * 2 + 1)
        return input_field

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Ошибка ввода")
        error_dialog.setText(message)
        error_dialog.exec_()

    def start_simulation(self):
        try:
            box_width = float(self.width_input.text())
            box_height = float(self.height_input.text())
            mass1 = float(self.mass1_input.text())
            velocity1_x = float(self.velocity1_x_input.text())
            velocity1_y = float(self.velocity1_y_input.text())
            x1 = float(self.x1_input.text())
            y1 = float(self.y1_input.text())
            mass2 = float(self.mass2_input.text())
            velocity2_x = float(self.velocity2_x_input.text())
            velocity2_y = float(self.velocity2_y_input.text())
            x2 = float(self.x2_input.text())
            y2 = float(self.y2_input.text())

            if any(val < 0 for val in [box_width, box_height, mass1, mass2, velocity1_x, velocity1_y, x1, y1, velocity2_x, velocity2_y, x2, y2]):
                raise ValueError("Все значения должны быть положительными.")
        except ValueError as e:
            self.show_error_message(str(e))
            return

        # Запуск симуляции
        body1 = Body(mass1, velocity1_x, velocity1_y, x1, y1, radius=0.5)
        body2 = Body(mass2, velocity2_x, velocity2_y, x2, y2, radius=0.5)
        dt = 0.01

        self.canvas.ax.clear()
        self.canvas.ax.set_xlim(0, box_width)
        self.canvas.ax.set_ylim(0, box_height)

        global body1_circle, body2_circle
        body1_circle, = self.canvas.ax.plot([], [], 'bo', markersize=20)
        body2_circle, = self.canvas.ax.plot([], [], 'ro', markersize=20)

        def animate(i):
            body1.update_position(dt)
            body2.update_position(dt)
            collision_with_wall(body1, box_width, box_height)
            collision_with_wall(body2, box_width, box_height)
            elastic_collision(body1, body2)
            body1_circle.set_data([body1.x], [body1.y])
            body2_circle.set_data([body2.x], [body2.y])
            return body1_circle, body2_circle

        self.ani = animation.FuncAnimation(self.canvas.fig, animate, frames=1000, interval=20, blit=True)
        self.canvas.draw()

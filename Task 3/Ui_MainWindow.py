import numpy as np
import matplotlib.animation as animation
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QPushButton, QComboBox, QDoubleSpinBox, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MainWindow")
        self.setGeometry(200, 100, 1500, 900)
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout(self.central_widget)
        
        self.label1 = QLabel("Ввод данных")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label1.setFont(font)
        self.label1.setAlignment(Qt.AlignTop)
        self.label1.setAlignment(Qt.AlignHCenter)
        self.label1.setStyleSheet("color: #2E8B57; padding: 10px;")
        layout.addWidget(self.label1, 0, 0, 1, 2)

        self.radius_label = QLabel("Введите радиус колеса (в метрах):")
        self.radius_label.setStyleSheet("color: #333; font-size: 12px; padding: 5px;")
        self.radius_input = QDoubleSpinBox()
        self.radius_input.setRange(0.1, 1000)
        self.radius_input.setValue(1.0)
        self.radius_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                # background-color: #4CAF50;
                border-radius: 1px;
            }
        """)
        layout.addWidget(self.radius_label, 1, 0)
        layout.addWidget(self.radius_input, 1, 1)

        self.velocity_label = QLabel("Введите скорость центра масс (в м/с):")
        self.velocity_label.setStyleSheet("color: #333; font-size: 12px; padding: 5px;")
        self.velocity_input = QDoubleSpinBox()
        self.velocity_input.setRange(0.1, 1000)
        self.velocity_input.setValue(1.0)
        self.velocity_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                # background-color: #4CAF50;
                border-radius: 1px;
            }
        """)
        layout.addWidget(self.velocity_label, 2, 0)
        layout.addWidget(self.velocity_input, 2, 1)

        self.model_label = QLabel("Выберите модель:")
        self.model_label.setStyleSheet("color: #333; font-size: 12px; padding: 5px;")
        self.model_select = QComboBox()
        self.model_select.addItem("Статическая")
        self.model_select.addItem("Динамическая")
        self.model_select.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                # background-color: #4CAF50;
                # width: 20px;
            }
        """)
        layout.addWidget(self.model_label, 3, 0)
        layout.addWidget(self.model_select, 3, 1)

        self.start_button = QPushButton("Перейти к отрисовке графика")
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                height: 40px;
                width: 200px;
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.start_model)
        layout.addWidget(self.start_button, 4, 0, 1, 2)

        self.canvas = None

    def set_background_image(self):
        background_image_path = "your_image_path.jpg"

        if not QtCore.QFile.exists(background_image_path):
            print(f"Ошибка: Изображение по пути '{background_image_path}' не найдено.")
            return

        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url({background_image_path});
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;  /* Растянуть изображение по окну */
                background-color: rgba(255, 255, 255, 0.8);  /* Белый фон с прозрачностью 0.8 */
            }}
        """)

    def start_model(self):
        R = self.radius_input.value()
        V = self.velocity_input.value()
        model_type = self.model_select.currentText()

        omega = V / R

        t_max = 50
        dt = 0.1
        t = np.arange(0, t_max, dt)

        x = V * t - R * np.sin(omega * t)
        y = R - R * np.cos(omega * t)

        if self.canvas is not None:
            self.canvas.setParent(None)

        if model_type == "Статическая":
            self.static_model(x, y)
        elif model_type == "Динамическая":
            self.dynamic_model(x, y, R, V, t, omega)

    def static_model(self, x, y):
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x, y, label="Траектория точки (циклоида)", color='red')
        ax.axhline(y=0, color='black', linestyle='--', label="Уровень земли")
        ax.set_xlabel("x (м)")
        ax.set_ylabel("y (м)")
        ax.set_title("Статическая модель: Траектория точки на ободе колеса (циклоида)")
        ax.legend()
        ax.grid(True)

        layout = self.central_widget.layout()
        layout.addWidget(self.canvas, 5, 0, 2, 2)
        self.canvas.draw()

    def dynamic_model(self, x, y, R, V, t, omega):
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        ax = self.canvas.figure.add_subplot(111)
        x_max = V * t.max()  # Максимальный предел по оси x
        ax.set_xlim(0, x_max)
        ax.set_ylim(-R, 2 * R)

        ax.set_xlabel("x (м)")
        ax.set_ylabel("y (м)")

        line_point, = ax.plot([], [], 'o', label="Точка на ободе", color='red')  # Точка на ободе
        line_path, = ax.plot([], [], '-', color='red', label="Траектория")  # Траектория
        ax.axhline(y=0, color='black', linestyle='--', label="Уровень земли")
        ax.legend()
        ax.grid(True)

        path_x = []
        path_y = []

        layout = self.central_widget.layout()
        layout.addWidget(self.canvas, 5, 0, 2, 2)

        def init():
            line_point.set_data([], [])
            line_path.set_data([], [])
            return line_point, line_path

        def animate(i):
            if i >= len(t):
                return line_point, line_path

            x_current = V * t[i] - R * np.sin(omega * t[i])
            y_current = R - R * np.cos(omega * t[i])
            path_x.append(x_current)
            path_y.append(y_current)

            line_point.set_data([x_current], [y_current])
            line_path.set_data(path_x, path_y)

            return line_point, line_path

        ani = animation.FuncAnimation(self.canvas.figure, animate, init_func=init, frames=len(t), interval=50,
                                      blit=True, repeat=False)
        self.canvas.draw()

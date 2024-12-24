import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QComboBox,
                             QMessageBox, QDialog)


class ResultsWindow(QDialog):
    """
    Класс для отображения результатов расчёта токов в электрической цепи.
    """

    def __init__(self, results, parent=None):
        """
        Инициализирует окно с результатами.

        :param results: Список строк с результатами расчётов.
        :param parent: Родительский объект окна.
        """
        super().__init__(parent)
        self.setWindowTitle("Результаты расчёта токов")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Рассчитанные токи:"))

        for line in results:
            layout.addWidget(QLabel(line))

        close_button = QPushButton("Закрыть")
        close_button.setStyleSheet("background-color: green; color: white;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


class ElectricCircuit:
    """
    Класс для представления электрической цепи и расчёта её параметров.
    """

    def __init__(self):
        """
        Инициализирует пустую электрическую цепь.
        """
        self.graph = nx.DiGraph()
        self.elements = {}
        self.voltage_sources = []

    def reset(self):
        """
        Сбрасывает граф и данные цепи.
        """
        self.graph = nx.DiGraph()
        self.elements = {}
        self.voltage_sources = []

    def add_resistor(self, node1, node2, resistance):
        """
        Добавляет резистор в цепь.

        :param node1: Начальный узел.
        :param node2: Конечный узел.
        :param resistance: Сопротивление резистора (Ом).
        """
        self.graph.add_edge(node1, node2, type='resistor', value=resistance)
        self.elements[(node1, node2)] = f"R={resistance}Ω"

    def add_voltage_source(self, node1, node2, voltage):
        """
        Добавляет источник напряжения в цепь.

        :param node1: Начальный узел.
        :param node2: Конечный узел.
        :param voltage: Значение напряжения (Вольт).
        """
        vs_name = f"V_{len(self.voltage_sources) + 1}"
        self.voltage_sources.append({'name': vs_name, 'node1': node1, 'node2': node2, 'value': voltage})
        self.graph.add_edge(node1, node2, type='voltage_source', value=voltage, name=vs_name)
        self.elements[(node1, node2, vs_name)] = f"E={voltage}В"

    def calculate_currents(self):
        """
        Рассчитывает токи в цепи, используя метод узлового анализа.

        :return: Словари с потенциалами узлов и токами через элементы.
        :raises np.linalg.LinAlgError: Если система уравнений вырождена.
        """
        nodes = list(self.graph.nodes())
        num_nodes = len(nodes)
        node_index = {node: idx for idx, node in enumerate(nodes)}
        reference_node = nodes[-1]
        ref_idx = node_index[reference_node]
        voltage_sources = self.voltage_sources
        num_vs = len(voltage_sources)
        size = (num_nodes - 1) + num_vs
        A = np.zeros((size, size))
        b = np.zeros(size)

        for edge in self.graph.edges(data=True):
            u, v, data = edge
            if data['type'] == 'resistor':
                resistance = data['value']
                conductance = 1 / resistance
                if u != reference_node:
                    A[node_index[u] if node_index[u] < ref_idx else node_index[u] - 1][
                        node_index[u] if node_index[u] < ref_idx else node_index[u] - 1] += conductance
                if v != reference_node:
                    A[node_index[v] if node_index[v] < ref_idx else node_index[v] - 1][
                        node_index[v] if node_index[v] < ref_idx else node_index[v] - 1] += conductance
                if u != reference_node and v != reference_node:
                    A[node_index[u] if node_index[u] < ref_idx else node_index[u] - 1][
                        node_index[v] if node_index[v] < ref_idx else node_index[v] - 1] -= conductance
                    A[node_index[v] if node_index[v] < ref_idx else node_index[v] - 1][
                        node_index[u] if node_index[u] < ref_idx else node_index[u] - 1] -= conductance
            elif data['type'] == 'voltage_source':
                vs = next((vs for vs in voltage_sources if vs['name'] == data['name']), None)
                if vs:
                    vs_idx = voltage_sources.index(vs)
                    if u != reference_node:
                        A[node_index[u] if node_index[u] < ref_idx else node_index[u] - 1][
                            (num_nodes - 1) + vs_idx] += 1
                    if v != reference_node:
                        A[node_index[v] if node_index[v] < ref_idx else node_index[v] - 1][
                            (num_nodes - 1) + vs_idx] -= 1
                    A[(num_nodes - 1) + vs_idx][node_index[u] if node_index[u] < ref_idx else node_index[u] - 1] = 1
                    A[(num_nodes - 1) + vs_idx][node_index[v] if node_index[v] < ref_idx else node_index[v] - 1] = -1
                    b[(num_nodes - 1) + vs_idx] = data['value']

        try:
            solution = np.linalg.solve(A, b)
            potentials = {}
            for node in nodes:
                if node == reference_node:
                    potentials[node] = 0
                else:
                    idx = node_index[node]
                    potentials[node] = solution[idx - 1] if idx > ref_idx else solution[idx]
            currents = {}
            for edge in self.graph.edges(data=True):
                u, v, data = edge
                if data['type'] == 'resistor':
                    current = (potentials[u] - potentials[v]) / data['value']
                    currents[(u, v)] = current
            for i, vs in enumerate(voltage_sources):
                vs_current = solution[(num_nodes - 1) + i]
                currents[(vs['node1'], vs['node2'], vs['name'])] = vs_current
            return potentials, currents
        except np.linalg.LinAlgError:
            raise np.linalg.LinAlgError("Система уравнений вырождена. Проверьте конфигурацию цепи.")

    def visualize_circuit(self):
        """
        Визуализирует граф электрической цепи.
        """
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(10, 8))
        edge_labels = {
            (u, v): f"{data['type']} {data['value']}" for u, v, data in self.graph.edges(data=True)
        }
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10,
                font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=10)
        plt.title("Визуализация электрической цепи")
        plt.show()


class ElectricCircuitGUI(QWidget):
    """
    Класс для графического интерфейса управления электрической цепью.
    """

    def __init__(self):
        """
        Инициализирует интерфейс приложения.
        """
        super().__init__()
        self.initUI()
        self.circuit = ElectricCircuit()
        self.fields = []

    def initUI(self):
        """
        Создаёт графический интерфейс.
        """
        self.setWindowTitle("Электрическая цепь")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        self.header = QLabel("Ввод данных", self)
        self.header.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
        layout.addWidget(self.header)
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Количество элементов:"), 0, 0)
        self.num_elements_input = QLineEdit()
        self.grid.addWidget(self.num_elements_input, 0, 1)
        self.add_elements_button = QPushButton("Создать поля")
        self.add_elements_button.setStyleSheet("background-color: green; color: white;")
        self.add_elements_button.clicked.connect(self.create_fields)
        self.grid.addWidget(self.add_elements_button, 0, 2)
        layout.addLayout(self.grid)
        self.elements_layout = QVBoxLayout()
        layout.addLayout(self.elements_layout)
        self.calculate_button = QPushButton("Рассчитать токи")
        self.calculate_button.setStyleSheet("background-color: green; color: white;")
        self.calculate_button.clicked.connect(self.calculate_currents)
        self.calculate_button.setEnabled(False)
        layout.addWidget(self.calculate_button)
        self.visualize_button = QPushButton("Визуализировать цепь")
        self.visualize_button.setStyleSheet("background-color: green; color: white;")
        self.visualize_button.clicked.connect(self.visualize_circuit)
        self.visualize_button.setEnabled(False)
        layout.addWidget(self.visualize_button)
        self.setLayout(layout)

    def create_fields(self):
        """
        Создаёт поля ввода для элементов цепи.
        """
        try:
            num_elements = int(self.num_elements_input.text())
            if num_elements <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректное количество элементов.")
            return
        for field in self.fields:
            for widget in field:
                widget.deleteLater()
        self.fields = []
        for i in range(num_elements):
            element_type = QComboBox()
            element_type.addItems(["Резистор", "Источник напряжения"])
            start_node = QLineEdit()
            end_node = QLineEdit()
            value = QLineEdit()
            self.grid.addWidget(QLabel(f"Элемент {i + 1} - Тип:"), i + 1, 0)
            self.grid.addWidget(element_type, i + 1, 1)
            self.grid.addWidget(QLabel("Начальный узел:"), i + 1, 2)
            self.grid.addWidget(start_node, i + 1, 3)
            self.grid.addWidget(QLabel("Конечный узел:"), i + 1, 4)
            self.grid.addWidget(end_node, i + 1, 5)
            self.grid.addWidget(QLabel("Значение (Ом/В):"), i + 1, 6)
            self.grid.addWidget(value, i + 1, 7)
            self.fields.append((element_type, start_node, end_node, value))
        self.calculate_button.setEnabled(True)
        self.visualize_button.setEnabled(True)

    def calculate_currents(self):
        """
        Вычисляет токи в цепи на основе введённых данных.
        """
        try:
            self.circuit.reset()
            for element_type, start_node, end_node, value in self.fields:
                node1 = start_node.text().strip()
                node2 = end_node.text().strip()
                val_text = value.text().strip()
                if not node1 or not node2 or not val_text:
                    raise ValueError("Заполните все поля элементов.")
                try:
                    val = float(val_text)
                except ValueError:
                    raise ValueError("Значение должно быть числом.")
                if element_type.currentText() == "Резистор":
                    if val <= 0:
                        raise ValueError("Сопротивление должно быть положительным.")
                    self.circuit.add_resistor(node1, node2, val)
                elif element_type.currentText() == "Источник напряжения":
                    self.circuit.add_voltage_source(node1, node2, val)
            potentials, currents = self.circuit.calculate_currents()
            result_lines = [f"Потенциал узлов:"]
            for node, pot in potentials.items():
                result_lines.append(f"V({node}) = {pot:.2f} В")
            result_lines.append("\nТоки через элементы:")
            for (u, v, *rest), current in currents.items():
                if rest:
                    element = self.circuit.elements.get((u, v, rest[0]), "Источник напряжения")
                else:
                    element = self.circuit.elements.get((u, v), "Резистор")
                result_lines.append(f"{element} ({u} -> {v}): {current:.2f} А")
            results_window = ResultsWindow(result_lines, self)
            results_window.exec_()
        except np.linalg.LinAlgError:
            QMessageBox.warning(self, "Ошибка", "Система уравнений вырождена. Проверьте конфигурацию цепи.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при расчёте: {str(e)}")

    def visualize_circuit(self):
        """
        Визуализирует текущую электрическую цепь.
        """
        try:
            self.circuit.visualize_circuit()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при визуализации: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ElectricCircuitGUI()
    window.show()
    sys.exit(app.exec_())

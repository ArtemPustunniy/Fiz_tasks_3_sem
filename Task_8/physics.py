import numpy as np
import matplotlib.pyplot as plt


def plot_energy_transformations(m, k, c, x0, v0, t_end, dt=0.01):
    """
    Построение графиков кинетической, потенциальной и полной механической энергии системы.

    Параметры:
    m (float): Масса груза (в кг).
    k (float): Коэффициент жесткости пружины (в Н/м).
    c (float): Коэффициент сопротивления среды (в Н·с/м).
    x0 (float): Начальное смещение груза (в метрах).
    v0 (float): Начальная скорость груза (в м/с).
    t_end (float): Время моделирования (в секундах).
    dt (float): Шаг интегрирования по времени.
    """

    # Инициализация переменных
    t_values = np.arange(0, t_end, dt)
    x = x0
    v = v0

    # Списки для хранения значений энергий
    kinetic_energy = []
    potential_energy = []
    total_energy = []

    for t in t_values:
        # Кинетическая и потенциальная энергия на текущем шаге
        ke = 0.5 * m * v**2
        pe = 0.5 * k * x**2
        kinetic_energy.append(ke)
        potential_energy.append(pe)
        total_energy.append(ke + pe)

        # Численный метод Эйлера для обновления x и v
        dxdt = v
        dvdt = -(c / m) * v - (k / m) * x
        x += dxdt * dt
        v += dvdt * dt

    # Построение графиков энергий
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t_values, kinetic_energy, label="Кинетическая энергия", color="b")
    plt.title("Кинетическая энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(t_values, potential_energy, label="Потенциальная энергия", color="g")
    plt.title("Потенциальная энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(t_values, total_energy, label="Полная механическая энергия", color="r")
    plt.title("Полная механическая энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

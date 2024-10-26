import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def plot_energy_transformations(m, k, c, x0, v0, t_end):
    """
    Построение графиков кинетической, потенциальной и полной механической энергии системы.

    Параметры:
    m (float): Масса груза (в кг).
    k (float): Коэффициент жесткости пружины (в Н/м).
    c (float): Коэффициент сопротивления среды (в Н·с/м).
    x0 (float): Начальное смещение груза (в метрах).
    v0 (float): Начальная скорость груза (в м/с).
    t_end (float): Время моделирования (в секундах).
    """

    def damped_oscillator(t, y):
        """
        Определение дифференциального уравнения для демпфированного осциллятора.
        """
        x, v = y
        dxdt = v
        dvdt = -(c / m) * v - (k / m) * x
        return [dxdt, dvdt]

    t_span = (0, t_end)
    t_eval = np.linspace(0, t_end, 1000)
    sol = solve_ivp(damped_oscillator, t_span, [x0, v0], t_eval=t_eval)

    x = sol.y[0]
    v = sol.y[1]
    kinetic_energy = 0.5 * m * v**2
    potential_energy = 0.5 * k * x**2
    total_energy = kinetic_energy + potential_energy

    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t_eval, kinetic_energy, label="Кинетическая энергия", color="b")
    plt.title("Кинетическая энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(t_eval, potential_energy, label="Потенциальная энергия", color="g")
    plt.title("Потенциальная энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(t_eval, total_energy, label="Полная механическая энергия", color="r")
    plt.title("Полная механическая энергия от времени")
    plt.xlabel("Время (с)")
    plt.ylabel("Энергия (Дж)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


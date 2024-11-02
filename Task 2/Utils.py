import math
import numpy as np
import matplotlib.pyplot as plt


g = 9.81


def ballistic_motion(h, v0, angle_deg):
    angle_rad = math.radians(angle_deg)

    # Обнуляем горизонтальную скорость при угле 90 градусов
    if angle_deg == 90:
        v0x = 0
    else:
        v0x = v0 * math.cos(angle_rad)

    v0y = v0 * math.sin(angle_rad)

    t_flight = (v0y + math.sqrt(v0y ** 2 + 2 * g * h)) / g

    t = np.linspace(0, t_flight, num=500)
    x = v0x * t  # Если угол 90 градусов, x всегда будет 0
    y = h + v0y * t - 0.5 * g * t ** 2

    vx = v0x * np.ones_like(t)
    vy = v0y - g * t

    v = np.sqrt(vx ** 2 + vy ** 2)
    return t, x, y, v, vx, vy


def plot_trajectory(x, y):
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.title('Траектория движения тела')
    plt.xlabel('Горизонтальная координата (м)')
    plt.ylabel('Вертикальная координата (м)')
    plt.grid(True)
    plt.show()


def plot_velocity(t, v):
    plt.figure(figsize=(8, 6))
    plt.plot(t, v)
    plt.title('Зависимость скорости от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Скорость (м/с)')
    plt.grid(True)
    plt.show()


def plot_coordinates(t, x, y):
    plt.figure(figsize=(8, 6))
    plt.plot(t, x, label='x (горизонтальная координата)')
    plt.plot(t, y, label='y (вертикальная координата)')
    plt.title('Зависимость координат от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Координаты (м)')
    plt.legend()
    plt.grid(True)
    plt.show()

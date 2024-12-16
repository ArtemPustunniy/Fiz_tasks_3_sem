import numpy as np
import matplotlib.pyplot as plt


def calculate_refraction(e1, e2, angle_inc):
    angle_inc_rad = np.radians(angle_inc)
    angle_refr_rad = np.arctan(np.tan(angle_inc_rad) * (e1 / e2))
    d_ratio = e2 / e1
    return angle_inc_rad, angle_refr_rad, d_ratio


def generate_plot(epsilon1, epsilon2, angle_inc, e0):
    angle_inc_rad, angle_refr_rad, d_ratio = calculate_refraction(
        epsilon1, epsilon2, angle_inc
    )

    x = np.linspace(-2, 2, 100)

    y_inc_E = np.tan(angle_inc_rad) * x
    y_refr_E = np.tan(angle_refr_rad) * x

    y_inc_D = y_inc_E * d_ratio
    y_refr_D = y_refr_E * d_ratio

    plt.figure(figsize=(10, 6))

    plt.axhline(0, color="k", linestyle="--", linewidth=1)

    plt.plot(x[x <= 0], y_inc_E[x <= 0], color="b", label="E в среде 1")
    plt.plot(x[x >= 0], y_refr_E[x >= 0], color="r", label="E в среде 2")

    plt.plot(x[x <= 0], y_inc_D[x <= 0], color="c", linestyle="--", label="D в среде 1")
    plt.plot(
        x[x >= 0], y_refr_D[x >= 0], color="m", linestyle="--", label="D в среде 2"
    )

    plt.title("Преломление E и D на границе двух диэлектриков")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()

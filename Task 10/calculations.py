import numpy as np
import matplotlib.pyplot as plt


def plot_field(charges):
    x = np.linspace(-5, 5, 300)
    y = np.linspace(-5, 5, 300)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros(X.shape)
    Ey = np.zeros(Y.shape)

    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        rx = X - x0
        ry = Y - y0
        r = np.sqrt(rx**2 + ry**2)
        r[r == 0] = 1e-9
        Ex += q * rx / r**3
        Ey += q * ry / r**3

    E = np.sqrt(Ex**2 + Ey**2)

    Ex /= E
    Ey /= E

    plt.figure(figsize=(10, 8))
    plt.streamplot(X, Y, Ex, Ey, color=np.log(E + 1), linewidth=1.5, cmap="hsv", density=2.0)
    plt.colorbar(label="Магнитуда электрического поля (логарифм)")

    for charge in charges:
        x0, y0 = charge["pos"]
        plt.scatter(x0, y0, color=charge["color"], s=200, edgecolor="black")

    plt.title("Электростатическое поле введенных зарядов")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.show()

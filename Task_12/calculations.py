import numpy as np


def calculate_field(X, Y, charges):
    Ex = np.zeros(X.shape)
    Ey = np.zeros(Y.shape)
    V = np.zeros(X.shape)

    for charge in charges:
        q = charge["q"]
        x0, y0 = charge["pos"]
        rx = X - x0
        ry = Y - y0
        r = np.sqrt(rx**2 + ry**2)
        r[r == 0] = 1e-9
        Ex += q * rx / r**3
        Ey += q * ry / r**3
        V += q / r

    return Ex, Ey, V

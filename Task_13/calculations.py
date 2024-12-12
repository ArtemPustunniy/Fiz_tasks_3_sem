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


def calculate_dipole_effect(X, Y, Ex, Ey, dipole):
    dipole_x, dipole_y = dipole["pos"]
    px, py = dipole["moment"]

    dipole_ex = np.interp(dipole_x, X[0], Ex[:, 0])
    dipole_ey = np.interp(dipole_y, Y[:, 0], Ey[0, :])

    force_x = px * dipole_ex
    force_y = py * dipole_ey
    torque = px * dipole_ey - py * dipole_ex

    return force_x, force_y, torque

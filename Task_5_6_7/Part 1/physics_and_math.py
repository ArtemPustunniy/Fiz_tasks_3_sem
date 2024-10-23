import numpy as np


def calculate_trajectory(v0, theta, h0, k, m=1.0, g=9.81, dt=0.01, t_max=10):
    """
    Calculates the trajectory of a body thrown at an angle to the horizontal, taking air resistance into account.

    Parameters:
    v0 -- initial velocity (m/s)
    theta -- angle between the velocity vector and the horizontal (degrees)
    h0 -- initial height from which the body is thrown (m)
    k -- air resistance coefficient
    m -- mass of the body (default is 1.0 kg)
    g -- gravitational acceleration (default is 9.81 m/s^2)
    dt -- time step for the numerical method (default is 0.01 s)
    t_max -- maximum simulation time (default is 10 s)

    Returns:
    x -- list of x coordinates of the body over time
    y -- list of y coordinates (height) of the body over time
    t -- list of time points corresponding to each position
    vx -- list of x components of velocity over time
    vy -- list of y components of velocity over time
    """
    # Convert angle to radians for trigonometric functions
    theta_rad = np.radians(theta)

    # Initial velocities in the x and y directions
    vx0 = v0 * np.cos(theta_rad)
    vy0 = v0 * np.sin(theta_rad)

    # Initialize lists for positions, velocities, and time
    x, y = [0], [h0]  # Initial position at t = 0
    vx, vy = [vx0], [vy0]  # Initial velocity components
    t = [0]  # Time starts at 0

    # Iterate while the body is above ground level (y >= 0) and within the maximum time
    while y[-1] >= 0 and t[-1] <= t_max:
        # Compute the total velocity magnitude at the current step
        v = np.sqrt(vx[-1] ** 2 + vy[-1] ** 2)

        # Update velocities based on air resistance and gravity (Euler's method)
        vx_new = vx[-1] - (k / m) * vx[-1] * dt  # Air resistance in x direction
        vy_new = vy[-1] - g * dt - (k / m) * vy[-1] * dt  # Gravity + air resistance in y direction

        # Update positions based on current velocities
        x_new = x[-1] + vx[-1] * dt  # New x position
        y_new = y[-1] + vy[-1] * dt  # New y position (height)

        # Update time
        t_new = t[-1] + dt

        # Append new values to the lists
        x.append(x_new)
        y.append(y_new)
        vx.append(vx_new)
        vy.append(vy_new)
        t.append(t_new)

    # Return the lists of positions, velocities, and time points
    return x, y, t, vx, vy

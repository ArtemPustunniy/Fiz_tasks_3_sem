def validate_input(v0, theta, h0, k):
    """
    Validates the user input for the projectile motion simulation.

    This function checks whether the entered values for initial velocity,
    angle, height, and air resistance coefficient are within valid ranges.
    If any of the values are invalid, an appropriate error message is added
    to the errors list.

    Parameters:
    ----------
    v0 : float
        Initial velocity (m/s). Must be a positive value.
    theta : float
        Angle between the velocity vector and the horizontal (degrees).
        Must be within the range [0, 90].
    h0 : float
        Initial height from which the body is thrown (m). Must be non-negative.
    k : float
        Air resistance coefficient. Must be non-negative.

    Returns:
    ----------
    errors : list of str
        A list containing error messages for each invalid parameter.
        If there are no errors, the list will be empty.
    """

    errors = []

    # Validate initial velocity (must be positive)
    if v0 <= 0:
        errors.append("Начальная скорость должна быть положительной.")  # "Initial velocity must be positive."

    # Validate angle (must be between 0 and 90 degrees)
    if not (0 <= theta <= 90):
        errors.append("Угол должен быть в диапазоне от 0 до 90 градусов.")  # "Angle must be between 0 and 90 degrees."

    # Validate initial height (must be non-negative)
    if h0 < 0:
        errors.append("Начальная высота не может быть отрицательной.")  # "Initial height cannot be negative."

    # Validate air resistance coefficient (must be non-negative)
    if k < 0:
        errors.append("Коэффициент сопротивления не может быть отрицательным.")  # "Air resistance coefficient cannot be negative."

    return errors


# Projectile Motion Simulation with Air Resistance

This project provides a graphical interface for simulating the motion of a projectile with air resistance using the PyQt5 framework. The application allows the user to input initial velocity, launch angle, initial height, and air resistance coefficient to simulate the trajectory of the projectile and visualize the results using `matplotlib`.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Files Structure](#files-structure)
4. [Dependencies](#dependencies)
5. [Features](#features)
6. [How It Works](#how-it-works)
7. [Validation](#validation)
8. [Notes](#notes)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/projectile-simulation.git
   cd projectile-simulation
   ```

2. **Install the required Python packages:**

   This project requires some additional Python packages such as PyQt5, NumPy, and Matplotlib. You can install them by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   After installation, you can run the application with:

   ```bash
   python main.py
   ```

## Usage

1. Launch the application. A window will appear with several input fields.
   
2. Enter the following values:
   - Initial velocity (in meters per second).
   - Launch angle (in degrees).
   - Initial height (in meters).
   - Air resistance coefficient (k).
   
3. Click the "Запустить симуляцию" (Run simulation) button to start the simulation. The application will validate the inputs and calculate the projectile's motion based on the provided values.

4. The application will display four graphs:
   - The projectile's trajectory (height vs. distance).
   - The velocity over time.
   - The x-coordinate over time.
   - The y-coordinate over time.

## Files Structure

```
projectile-simulation/
│
├── main.py                # Main file to launch the PyQt application
├── physics_and_math.py     # Contains the trajectory calculation logic
├── validation.py           # Handles input validation
├── requirements.txt        # Required Python libraries
└── README.md               # This file
```

## Dependencies

The project requires the following Python libraries:

- **PyQt5**: For building the graphical user interface.
- **Matplotlib**: For plotting the simulation results.
- **NumPy**: For numerical computations in the simulation.
  
You can install these dependencies by running `pip install -r requirements.txt`.

## Features

- **Graphical User Interface**: The app uses PyQt5 to create a user-friendly interface where the user can input initial parameters for the projectile motion simulation.
  
- **Input Validation**: The app validates user input to ensure that values entered are numeric and within valid ranges. Errors are displayed in a dialog box for the user to correct.

- **Air Resistance Simulation**: The simulation takes air resistance into account, affecting the trajectory of the projectile.

- **Visualization**: The results of the simulation are displayed using `matplotlib` as graphs that show the trajectory, velocity, and time dependencies of the x and y coordinates.

## How It Works

1. **Input**: The user provides the initial velocity, launch angle, height, and air resistance coefficient via the PyQt5 interface.

2. **Validation**: The `validate_input` function ensures that all inputs are valid (i.e., numeric and within reasonable ranges). If invalid input is detected, the user is shown an error dialog box.

3. **Simulation**: The `calculate_trajectory` function computes the projectile's motion by solving the equations of motion numerically. It takes into account air resistance, using Euler's method for time integration.

4. **Plotting**: The `plot_trajectory` function visualizes the results using `matplotlib`. Four graphs are plotted:
   - Trajectory of the projectile (x vs. y).
   - Velocity as a function of time.
   - x-coordinate as a function of time.
   - y-coordinate as a function of time.

## Validation

Validation is performed by the `validate_input` function from the `validation.py` file. It checks whether the inputs are:
- Numeric values.
- Positive values for velocity, height, and air resistance coefficient.

If the validation fails, a warning dialog is shown with the corresponding error messages.

## Notes

- **Air resistance**: The air resistance is modeled as proportional to the velocity, with the resistance coefficient `k` affecting the drag force. The higher the coefficient, the more the projectile is affected by drag.
  
- **Euler's method**: The simulation uses Euler's method for time-stepping the projectile's motion. A small time step (`dt = 0.01`) is used to ensure accuracy.

- **Limitations**: The simulation assumes that the mass of the projectile is constant and that the air resistance is a simple linear function of velocity.

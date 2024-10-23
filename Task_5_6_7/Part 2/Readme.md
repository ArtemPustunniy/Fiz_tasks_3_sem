
# Potential Energy Simulation

This project provides a graphical interface for simulating potential energy fields from different types of forces using the PyQt5 framework. The user can select various forces such as gravity, elastic (spring) forces, weight, and even add unknown forces modeled as power functions of coordinates. The potential energy field is visualized using `matplotlib`.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Files Structure](#files-structure)
4. [Dependencies](#dependencies)
5. [Features](#features)
6. [How It Works](#how-it-works)
7. [Notes](#notes)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/potential-simulation.git
   cd potential-simulation
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

1. Launch the application. A window will appear with checkboxes to select the forces to include in the simulation.
   
2. Select one or more of the following forces:
   - Elastic (spring) force.
   - Gravitational force.
   - Weight force.
   - Unknown forces (you can specify the coefficients and exponents for each unknown force).
   
3. Click the "Next" button to proceed to the input window. Input the necessary parameters for the selected forces, such as the spring constant, mass, gravitational acceleration, and weight.

4. If unknown forces are selected, input the number of unknown forces and specify the parameters for each.

5. Click the "Run Simulation" button to calculate the potential field. The results will be visualized as a contour plot of the potential energy.

## Files Structure

```
potential-simulation/
│
├── main.py                # Main file to launch the PyQt application
├── potential_calculations.py     # Contains the potential energy calculation logic
├── requirements.txt        # Required Python libraries
└── README.md               # This file
```

## Dependencies

The project requires the following Python libraries:

- **PyQt5**: For building the graphical user interface.
- **Matplotlib**: For plotting the potential energy field.
- **NumPy**: For numerical computations in the simulation.
  
You can install these dependencies by running `pip install -r requirements.txt`.

## Features

- **Graphical User Interface**: The app uses PyQt5 to create an intuitive interface where the user can select forces and input the corresponding parameters.
  
- **Unknown Forces**: The app allows the user to define an arbitrary number of unknown forces as power functions of coordinates. This provides flexibility in simulating various potential fields.

- **Visualization**: The results of the simulation are displayed as a contour plot showing the total potential energy field.

## How It Works

1. **Force Selection**: The user selects the forces they wish to include in the simulation, such as spring, gravity, or weight forces.

2. **Input Parameters**: The user inputs parameters specific to each force, such as the spring constant for the spring force or the mass and gravitational acceleration for gravity.

3. **Unknown Forces**: If the user selects unknown forces, they can specify the coefficients and exponents for each unknown force.

4. **Simulation**: The potential energy field is calculated based on the selected forces. The application uses `numpy` for numerical computations and solves the potential field on a grid.

5. **Plotting**: The resulting potential energy field is visualized using `matplotlib` as a contour plot, where the user can see the distribution of potential energy across the grid.

## Notes

- **Force Combinations**: The application allows any combination of forces, making it versatile for various simulations.

- **Unknown Forces**: The unknown forces can be defined as power functions of coordinates with customizable coefficients and exponents, which adds flexibility for more complex simulations.

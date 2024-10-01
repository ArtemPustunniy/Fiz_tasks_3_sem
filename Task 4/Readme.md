# Simulation of Body Movement and Collisions

This project is a Python-based simulation of two bodies moving and colliding within a rectangular container. The simulation uses PyQt5 for the graphical user interface (GUI) and Matplotlib to visualize the movement of the bodies. The physics of the system includes wall collisions and elastic collisions between the bodies.

## Features

- Simulates the movement of two bodies within a rectangular box.
- Supports elastic collisions between bodies based on their mass, velocity, and position.
- Handles collisions with the walls of the container.
- Graphical user interface built using PyQt5.
- Visualization of the simulation using Matplotlib.

## Project Structure

```bash
project/
├── main.py             # Main entry point for the application
├── logic.py            # Physics logic for movement and collisions
└── ui.py               # User interface logic

# Trail Formation Agent-Based Model

This project implements an agent-based model (ABM) using Mesa to simulate the formation of walking trails on a landscape with terrain and trees. The model demonstrates how human movement patterns can create emergent trail networks based on terrain characteristics and points of interest.

## Features

- Digital Elevation Model (DEM) representation of terrain
- Tree distribution on the landscape
- Agents that move between points of interest
- Trail formation based on terrain characteristics and agent behavior
- Visualization of the landscape, trees, and emerging trails

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt

## Installation

1. Clone this repository
2. Create a virtual environment (recommended)
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the model with visualization:
```bash
python run.py
```

## Model Components

- `model.py`: Contains the main model class and landscape setup
- `agents.py`: Defines the agent behavior and movement rules
- `run.py`: Main script to run the simulation
- `visualization.py`: Handles the visualization of the model 
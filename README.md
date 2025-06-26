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

This project uses `uv` for package management. `uv` is an extremely fast Python package installer and resolver, written in Rust, and designed as a drop-in replacement for `pip` and `pip-tools`.

1. **Install `uv`**

   You can install `uv` using the following command:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or, if you have `pipx`:
   ```bash
   pipx install uv
   ```

2. **Create a virtual environment**
   ```bash
   uv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   uv pip sync requirements.txt
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
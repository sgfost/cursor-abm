# Trail Formation Agent-Based Model: Documentation

This document provides a detailed explanation of the agent-based model (ABM) for simulating trail formation. It covers the model's purpose, its components, and how it functions.

## 1. Simulation Purpose and Overview

The primary purpose of this simulation is to model and visualize how walking trails emerge on a landscape as a result of agent movement. The model demonstrates emergent behavior, where complex patterns (trail networks) arise from simple rules followed by individual agents.

The simulation is built on a grid-based environment that includes:
- A digital elevation model (DEM) representing terrain with varying slopes.
- A distribution of trees that act as obstacles.
- Designated "points of interest" that agents travel between.

Agents (or "Walkers") navigate this environment, attempting to find the most efficient path between points of interest. Their movement choices are influenced by the terrain, the presence of existing trails, and the direct-line distance to their destination. Over time, as many agents traverse the landscape, their repeated paths create a visible network of trails.

## 2. Model Components and Variables

### 2.1. Environment

The environment is a 2D grid with several key properties:

- **Dimensions**: `width` and `height` define the size of the simulation area.
- **Terrain (`self.terrain`)**: A 2D NumPy array representing the elevation at each grid cell. It is generated using Perlin noise with a Gaussian filter to create a smooth, natural-looking landscape. Elevation values are normalized between 0 and 1.
- **Trees (`self.trees`)**: A 2D boolean NumPy array indicating the presence of trees. Trees are placed randomly, with a constraint to prevent them from clumping too closely together. Agents cannot move into cells occupied by trees.
- **Points of Interest (`self.points_of_interest`)**: A list of coordinates representing locations that agents are motivated to travel between. These are created at the start of the simulation and are placed in locations without trees.

### 2.2. Agents (`Walker`)

The agents are the active entities in the model. Each `Walker` has the following key attributes and behaviors:

- **Goal (`self.current_goal`)**: The coordinate of the point of interest the agent is currently moving towards. When an agent reaches its goal or has been walking for too long (`max_steps`), it chooses a new, random point of interest to travel to.
- **Movement Logic (`_move`)**: In each step, an agent considers all valid neighboring cells (Moore neighborhood, i.e., 8 adjacent cells). It calculates a "cost" for moving to each neighboring cell based on a combination of three factors:
    1.  **Terrain Cost**: The steepness of the slope between the current position and the potential next position. Steeper slopes have a higher cost, discouraging agents from climbing or descending sharp inclines. This is calculated in the `get_terrain_cost` method.
    2.  **Distance Cost**: The Euclidean distance from the potential next cell to the agent's current goal. This encourages agents to move in the general direction of their target.
    3.  **Trail Cost**: The strength of the trail in the potential next cell. Existing trails have a lower cost, encouraging agents to follow established paths.
- The agent always moves to the neighboring cell with the lowest total cost.

### 2.3. Interim and Output Variables

- **Trail Network (`self.trail_network`)**: This is a 2D NumPy array with the same dimensions as the grid. It represents the "strength" of the trail at each cell and is the primary output of the simulation.
    - **How it's updated**: Every time an agent moves to a new cell, it increases the trail strength at that location by a small amount (0.1). The trail strength is capped at a maximum value of 1.0.
    - **`_update_trail()`**: This method in the `Walker` class is responsible for updating the trail network.
- **Data Collector (`self.datacollector`)**: The model uses Mesa's `DataCollector` to track statistics over time. In this model, it records the `Trail_Density` at each step, which is the mean value of the `trail_network` array. This provides a high-level measure of how developed the trail system is.

## 3. How the Simulation Works

The simulation proceeds in discrete time steps. Here is a summary of the process:

1.  **Initialization**:
    - The `TrailModel` is instantiated with parameters for grid size, number of agents, and number of trees.
    - The terrain, trees, and points of interest are generated.
    - Agents are created and placed at random points of interest.
    - The `trail_network` is initialized as an array of zeros.

2.  **Simulation Step (`step`)**:
    - The model's `step` method is called at each time step.
    - It first calls the `collect` method of the data collector to record the current state of the model's reporters (in this case, `Trail_Density`).
    - Then, it calls the `step` method of the `RandomActivation` scheduler. This iterates through all the agents in a random order and executes each agent's `step` method.

3.  **Agent Behavior (`Walker.step`)**:
    - Each agent checks if it has a `current_goal`. If not, it chooses a new one from the list of available points of interest.
    - The agent then executes its `_move` logic to select the best next step and moves to that position on the grid.
    - After moving, the agent calls `_update_trail` to strengthen the trail at its new location.
    - Finally, the agent checks if it has reached its goal or if it has taken the maximum number of steps, and if so, it resets its goal for the next turn.

This process repeats for each time step, and over time, the `trail_network` evolves from a blank slate into a network of paths connecting the points of interest, shaped by the underlying terrain and the collective behavior of the agents. 
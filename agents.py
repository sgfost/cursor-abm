import numpy as np
from mesa import Agent

class Walker(Agent):
    def __init__(self, unique_id, model, start_point):
        super().__init__(model)
        self.unique_id = unique_id
        self.model = model
        self.current_goal = None
        self.path = []
        self.steps_taken = 0
        self.max_steps = 100  # Maximum steps before choosing a new goal
        
    def step(self):
        """Execute one step of the agent's behavior."""
        # If no current goal, choose one
        if self.current_goal is None:
            self._choose_new_goal()
        
        # Move towards the goal
        self._move()
        
        # Update trail network
        self._update_trail()
        
        # Check if we've reached the goal
        if self.pos == self.current_goal:
            self.current_goal = None
            self.steps_taken = 0
        
        # If we've been walking too long, choose a new goal
        self.steps_taken += 1
        if self.steps_taken >= self.max_steps:
            self.current_goal = None
            self.steps_taken = 0
    
    def _choose_new_goal(self):
        """Choose a new point of interest to walk to."""
        # Get all points except current position
        available_points = [p for p in self.model.points_of_interest if p != self.pos]
        
        if not available_points:
            return
        
        # Choose a random point
        self.current_goal = available_points[np.random.randint(len(available_points))]
    
    def _move(self):
        """Move towards the current goal."""
        if self.current_goal is None:
            return
        
        # Get possible next positions
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        
        # Filter out positions with trees
        possible_steps = [pos for pos in possible_steps 
                         if not self.model.trees[pos[0], pos[1]]]
        
        if not possible_steps:
            return
        
        # Calculate costs for each possible step
        costs = []
        for pos in possible_steps:
            # Cost based on terrain
            terrain_cost = self.model.get_terrain_cost(self.pos, pos)
            
            # Cost based on distance to goal
            dx = pos[0] - self.current_goal[0]
            dy = pos[1] - self.current_goal[1]
            distance_cost = np.sqrt(dx*dx + dy*dy)
            
            # Cost based on existing trails (prefer existing trails)
            trail_cost = 1 - self.model.trail_network[pos[0], pos[1]]
            
            # Total cost
            total_cost = terrain_cost + distance_cost + trail_cost
            costs.append(total_cost)
        
        # Choose the step with the lowest cost
        best_step = possible_steps[np.argmin(costs)]
        
        # Move to the chosen position
        self.model.grid.move_agent(self, best_step)
    
    def _update_trail(self):
        """Update the trail network based on agent movement."""
        # Increase trail strength at current position
        self.model.trail_network[self.pos[0], self.pos[1]] += 0.1
        
        # Cap the trail strength at 1
        self.model.trail_network[self.pos[0], self.pos[1]] = min(
            1.0, 
            self.model.trail_network[self.pos[0], self.pos[1]]
        ) 
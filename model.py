import numpy as np
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from scipy.ndimage import gaussian_filter
from agents import Walker

class TrailModel(Model):
    def __init__(self, width=50, height=50, num_agents=20, num_trees=100):
        super().__init__()
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.num_trees = num_trees
        
        # Create the grid
        self.grid = MultiGrid(width, height, True)
        
        # Initialize the schedule
        self.schedule = RandomActivation(self)
        
        # Create the landscape (DEM)
        self.terrain = self._generate_terrain()
        
        # Place trees
        self.trees = self._place_trees()
        
        # Create points of interest
        self.points_of_interest = self._create_points_of_interest()
        
        # Create agents
        self._create_agents()
        
        # Initialize trail network
        self.trail_network = np.zeros((width, height))
        
        # Data collector for statistics
        self.datacollector = DataCollector(
            model_reporters={"Trail_Density": lambda m: np.mean(m.trail_network)}
        )
        
    def _generate_terrain(self):
        """Generate a random terrain using Perlin noise and smoothing."""
        # Generate random noise
        noise = np.random.rand(self.width, self.height)
        
        # Apply Gaussian smoothing to create more natural-looking terrain
        terrain = gaussian_filter(noise, sigma=3)
        
        # Normalize to 0-1 range
        terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
        
        return terrain
    
    def _place_trees(self):
        """Place trees randomly on the landscape."""
        trees = np.zeros((self.width, self.height), dtype=bool)
        num_placed = 0
        
        while num_placed < self.num_trees:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            
            # Avoid placing trees too close to each other
            if not trees[max(0, x-2):min(self.width, x+3), 
                        max(0, y-2):min(self.height, y+3)].any():
                trees[x, y] = True
                num_placed += 1
        
        return trees
    
    def _create_points_of_interest(self):
        """Create points of interest that agents will travel between."""
        num_points = 5
        points = []
        
        for _ in range(num_points):
            while True:
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
                
                # Avoid placing points in trees or too close to other points
                if not self.trees[x, y] and not any(
                    abs(x - px) < 5 and abs(y - py) < 5 
                    for px, py in points
                ):
                    points.append((x, y))
                    break
        
        return points
    
    def _create_agents(self):
        """Create and place agents on the grid."""
        for i in range(self.num_agents):
            # Place agents at random points of interest
            start_point = self.points_of_interest[np.random.randint(len(self.points_of_interest))]
            agent = Walker(i, self, start_point)
            self.schedule.add(agent)
            self.grid.place_agent(agent, start_point)
    
    def step(self):
        """Advance the model by one step."""
        self.datacollector.collect(self)
        self.schedule.step()
    
    def get_terrain_cost(self, pos1, pos2):
        """Calculate the cost of moving between two positions based on terrain."""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Get terrain values
        terrain1 = self.terrain[x1, y1]
        terrain2 = self.terrain[x2, y2]
        
        # Calculate slope
        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return 0
            
        slope = abs(terrain2 - terrain1) / distance
        
        # Higher cost for steeper slopes
        return 1 + slope * 2 
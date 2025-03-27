from model import TrailModel
from visualization import create_visualization, plot_results
import solara

# Create the model
model = TrailModel(
    width=50,
    height=50,
    num_agents=20,
    num_trees=100
)

# Create the visualization
page = create_visualization(model)

# This is required to render the visualization
page 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mesa.visualization import SolaraViz, make_plot_component, make_space_component

def agent_portrayal(agent):
    """Define how agents are portrayed in the visualization."""
    return {
        "color": "red",
        "size": 50,
    }

def create_visualization(model):
    """Create the visualization server."""
    # Define model parameters
    model_params = {
        "width": {
            "type": "SliderInt",
            "value": 50,
            "label": "Width:",
            "min": 10,
            "max": 100,
            "step": 1,
        },
        "height": {
            "type": "SliderInt",
            "value": 50,
            "label": "Height:",
            "min": 10,
            "max": 100,
            "step": 1,
        },
        "num_agents": {
            "type": "SliderInt",
            "value": 20,
            "label": "Number of Agents:",
            "min": 1,
            "max": 100,
            "step": 1,
        },
        "num_trees": {
            "type": "SliderInt",
            "value": 100,
            "label": "Number of Trees:",
            "min": 0,
            "max": 500,
            "step": 1,
        }
    }
    
    # Create visualization components
    SpaceGraph = make_space_component(agent_portrayal)
    TrailPlot = make_plot_component("Trail_Density")
    
    # Create the visualization page
    page = SolaraViz(
        model,
        components=[SpaceGraph, TrailPlot],
        model_params=model_params,
        name="Trail Formation Model"
    )
    
    return page

def plot_results(model, steps=100):
    """Create a static plot of the model results."""
    # Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot terrain
    terrain_plot = ax1.imshow(model.terrain, cmap='terrain')
    ax1.set_title('Terrain')
    plt.colorbar(terrain_plot, ax=ax1)
    
    # Plot trees
    tree_plot = ax2.imshow(model.trees, cmap='binary')
    ax2.set_title('Trees')
    plt.colorbar(tree_plot, ax=ax2)
    
    # Plot trail network
    trail_plot = ax3.imshow(model.trail_network, cmap='YlOrRd')
    ax3.set_title('Trail Network')
    plt.colorbar(trail_plot, ax=ax3)
    
    plt.tight_layout()
    plt.show() 
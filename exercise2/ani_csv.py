import numpy as np
import os

grid_size = 20
inch = (grid_size - 2) // 9
time_steps = 200
simulation = "test_simulation_csv"

# Create the simulation folder
os.makedirs(simulation, exist_ok=True)

# Initialize the temperature grid
temperature_grid = np.full((grid_size, grid_size), 90.0)

temperature_grid[0, :] = 100
temperature_grid[grid_size - 1, :] = 32
gradient = np.linspace(100, 32, num=(5 * inch) + 2)
temperature_grid[1:(5 * inch) + 1, 0] = gradient[1:-1]
temperature_grid[(5 * inch):grid_size - 1, 0] = 32
temperature_grid[1:(5 * inch) + 1, grid_size - 1] = gradient[1:-1]
temperature_grid[(5 * inch):grid_size - 1, grid_size - 1] = 32

for i in range((3 * inch) + 1, (6 * inch) + 1):
    for j in range((3 * inch) + 1, (6 * inch) + 1):
        temperature_grid[i, j] = 212

# Function to update grid based on diffusion
def diffuse(grid):
    new_grid = grid.copy()
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            if (i in range((3 * inch) + 1, (6 * inch) + 1)) and (j in range((3 * inch) + 1, (6 * inch) + 1)):
                continue
            new_grid[i, j] = (grid[i + 1, j] + grid[i - 1, j] + grid[i, j + 1] + grid[i, j - 1]) / 4
    return new_grid

# Save a grid as a CSV file
def save_to_csv(grid, simulation, timestep):
    # Prepare the data: x, y, temperature
    x_coords, y_coords = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
    csv_data = np.column_stack((x_coords.ravel(), y_coords.ravel(), grid.ravel()))
    
    # Define the file name inside the folder
    file_name = os.path.join(simulation, f"temperature_timestep_{timestep:03d}.csv")
    
    # Write the CSV file
    header = "x,y,temperature"
    np.savetxt(file_name, csv_data, delimiter=",", header=header, comments="", fmt="%.2f")

# Perform diffusion and save results
for t in range(time_steps):
    print("timestep: ", t)
    save_to_csv(temperature_grid, simulation, t)
    temperature_grid = diffuse(temperature_grid)

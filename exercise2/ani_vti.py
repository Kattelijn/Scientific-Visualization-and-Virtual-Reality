import numpy as np
import vtk
import os

grid_size = 20
inch = (grid_size - 2) // 9
tolerance = 0.5
max_iterations = 100
simulation = "simulation_20x20"

os.makedirs(simulation, exist_ok=True)

temperature_grid = np.full((grid_size, grid_size), 90.0)

temperature_grid[0, :] = 100
temperature_grid[grid_size-1, :] = 32
gradient = np.linspace(100, 32, num=(5 * inch)+2)
temperature_grid[1:(5*inch)+1, 0] = gradient[1:-1]
temperature_grid[(5*inch)+1:grid_size-1, 0] = 32
temperature_grid[1:(5*inch)+1, grid_size-1] = gradient[1:-1]
temperature_grid[(5*inch)+1:grid_size-1, grid_size-1] = 32

for i in range((3 * inch) + 1, (6 * inch) + 1):
    for j in range((3 * inch) + 1, (6 * inch) + 1):
        temperature_grid[i, j] = 212

# Function to update grid based on diffusion
def diffuse(grid):

    new_grid = grid.copy()
    max_change = 0

    for i in range(1, grid_size - 1):
        for j in range(1, (grid_size//2)):
            if (i in range((3 * inch) + 1, (6 * inch) + 1)) and (j in range((3 * inch) + 1, (6 * inch) + 1)):
                continue
            new_grid[i, j] = (grid[i + 1, j] + grid[i - 1, j] + grid[i, j + 1] + grid[i, j - 1]) / 4
            change = abs(new_grid[i, j] - grid[i, j])
            if change > max_change:
                max_change = change
    
    new_grid[1:grid_size-1, (grid_size//2):grid_size-1] = np.fliplr(new_grid[1:grid_size-1, 1:(grid_size//2)])

    return new_grid, max_change

# Save a grid as a .vti file
def save_to_vti(grid, simulation, timestep):

    adjusted_grid = np.flipud(grid).T

    # Create a VTK image data object
    image_data = vtk.vtkImageData()
    image_data.SetDimensions(grid_size, grid_size, 1)
    image_data.AllocateScalars(vtk.VTK_FLOAT, 1)
    image_data.SetOrigin(0, 0, 0)
    
    # Populate the image data with the temperature grid
    for i in range(grid_size):
        for j in range(grid_size):
            image_data.SetScalarComponentFromFloat(i, j, 0, 0, adjusted_grid[i, j])
    
    # Define the file name inside the folder
    file_name = os.path.join(simulation, f"temperature_timestep_{timestep:03d}.vti")
    
    # Write the image data to a .vti file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(file_name)
    writer.SetInputData(image_data)
    writer.Write()

# Perform diffusion and save results
t = 0
max_change = 1000

while max_change > tolerance:
    print("timestep: ", t)
    save_to_vti(temperature_grid, simulation, t)
    temperature_grid, max_change = diffuse(temperature_grid)
    t += 1
    if t > max_iterations:
        break
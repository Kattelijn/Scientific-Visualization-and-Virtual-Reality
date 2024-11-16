import numpy as np
import matplotlib.pyplot as plt
import vtk

grid_size = 20
inch = (grid_size - 2) // 9
time_steps = 100

temperature_grid = np.zeros((grid_size, grid_size))

temperature_grid[0, :] = 100
temperature_grid[grid_size-1, :] = 32

gradient = np.linspace(100, 32, num=(5 * inch)+2)
temperature_grid[1:(5 * inch)+1, 0] = gradient[1:-1]
temperature_grid[(5*inch):grid_size-1, 0] = 32
temperature_grid[1:(5*inch)+1, grid_size-1] = gradient[1:-1]
temperature_grid[(5*inch):grid_size-1, grid_size-1] = 32

for i in range((3*inch)+1, (6*inch)+1):
    for j in range((3*inch)+1, (6*inch)+1):
        temperature_grid[i, j] = 212

# Function to update grid based on diffusion
def diffuse(grid):
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            # Calculate the diffusion based on neighboring cells
            grid[i, j] = (grid[i+1, j] + grid[i-1, j] + grid[i, j+1] + grid[i, j-1])/4
    for i in range((3*inch)+1, (6*inch)+1):
        for j in range((3*inch)+1, (6*inch)+1):
            temperature_grid[i, j] = 212

    return grid

temperature_grid = diffuse(diffuse(diffuse(diffuse(temperature_grid))))

# fig, ax = plt.subplots()
# cax = ax.imshow(temperature_grid, cmap='hot')
# fig.colorbar(cax)
# plt.show()


# Set up VTK objects
# Create a VTK image data to store the temperature grid
image_data = vtk.vtkImageData()
image_data.SetDimensions(grid_size, grid_size, 1)
image_data.AllocateScalars(vtk.VTK_FLOAT, 1)

# Set up the color lookup table
lookup_table = vtk.vtkLookupTable()
lookup_table.SetRange(0.0, 212.0)  # Temperature range
lookup_table.SetValueRange(0.0, 1.0)  # Brightness range
lookup_table.SetSaturationRange(1.0, 1.0)  # Saturation range
lookup_table.SetHueRange(0.0, 1.0)  # Color range from blue to red
lookup_table.Build()

# Map image data to colors using the lookup table
color_mapper = vtk.vtkImageMapToColors()
color_mapper.SetLookupTable(lookup_table)
color_mapper.SetInputData(image_data)

# Set up the actor to display the temperature grid
actor = vtk.vtkImageActor()
actor.GetMapper().SetInputConnection(color_mapper.GetOutputPort())

# Set up the renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Set up the render window
render_window = vtk.vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)

# Set up the interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Update the VTK image data with the current temperature grid
def update_image_data(grid):
    for i in range(grid_size):
        for j in range(grid_size):
            image_data.SetScalarComponentFromFloat(i, j, 0, 0, grid[i, j])

# Animation loop
def animation_callback(obj, event):
    global temperature_grid
    temperature_grid = diffuse(temperature_grid)
    update_image_data(temperature_grid)
    render_window.Render()

# Initialize the grid for rendering
update_image_data(temperature_grid)

# Add the animation callback
interactor.AddObserver('TimerEvent', animation_callback)
timer_id = interactor.CreateRepeatingTimer(50)  # 50 ms timer

# Start the interaction
interactor.Start()

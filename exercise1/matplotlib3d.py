import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import pandas as pd

# Load your dataset
df = pd.read_csv('cars.csv')

# Get unique years and origins to iterate through
years = sorted(df['year'].unique())
origins = df['origin'].unique()

# Color mapping for each origin
color_map = {'US': 'blue', 'Europe': 'green', 'Japan': 'red'}
df['color'] = df['origin'].map(color_map)

# Calculate min and max for each axis to keep points within frame
x_min, x_max = df['MPG'].min(), df['MPG'].max()
y_min, y_max = df['horsepower'].min(), df['horsepower'].max()
z_min, z_max = df['weigth'].min(), df['weigth'].max()  # Note change here

# Set up the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
title = ax.set_title('3D Car Data')

# Set fixed axis limits
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)

# Add axis labels
ax.set_xlabel("Miles Per Gallon (MPG)")
ax.set_ylabel("Horsepower")
ax.set_zlabel("Weight (lbs)")  # Axis label remains "Weight" for clarity

# Plot the entire dataset in the background with low opacity
ax.scatter(df['MPG'], df['horsepower'], df['weigth'], c=df['color'], alpha=0.1)

# Create a legend for origins
for origin, color in color_map.items():
    ax.scatter([], [], [], color=color, label=origin)  # Empty scatter for legend only
ax.legend(loc="upper left", title="Origin")

# Function to update the graph for each frame
def update_graph(num):
    year = years[num]  # Select the corresponding year for this frame
    data = df[df['year'] == year]
    
    # Clear previous highlighted points and re-plot for the specific year
    highlighted._offsets3d = (data['MPG'], data['horsepower'], data['weigth'])
    highlighted.set_color(data['color'])  # Color by origin
    title.set_text('Year = 19{}'.format(year))  # Update the title to show the current year

# Initial scatter plot for highlighted points (to update in animation)
data = df[df['year'] == years[0]]
highlighted = ax.scatter(data['MPG'], data['horsepower'], data['weigth'], c=data['color'], edgecolor='k')

# Create the animation, iterating over the years
ani = matplotlib.animation.FuncAnimation(fig, update_graph, frames=len(years), interval=500, blit=False)

ani.save("car_data_animation.mp4", writer='ffmpeg', fps=2)

plt.show()
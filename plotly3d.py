import pandas as pd
import plotly.express as px

df = pd.read_csv('cars.csv')

fig = px.scatter_3d(
    df,
    x="MPG",
    y="horsepower",
    z="weigth",
    animation_frame="year",
    color="origin",
    size="cylinders",
    hover_name="model",
    title="3D Car Data Animation",
    range_x=[0, df["MPG"].max() + 10],
    range_y=[0, df["horsepower"].max() + 50],
    range_z=[0, df["weigth"].max() + 500]
)

fig.show()

fig.write_html("car_data_3D_animation.html")


# TODO
# change years 70 -> 1970
# change representation of cylinders
# add background of all data
# buttons to select origin/cylinders
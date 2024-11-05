import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('cars.csv')

df["year"] = "19" + df["year"].astype(str)

size_factor = 2

fig = px.scatter_3d(
    df,
    x="MPG",
    y="horsepower",
    z="weigth",
    animation_frame="year",
    color="origin",
    size="cylinders",
    hover_name="model",
    #title="3D Car Data Animation",
    range_x=[0, df["MPG"].max() + 10],
    range_y=[0, df["horsepower"].max() + 50],
    range_z=[0, df["weigth"].max() + 500]
)

for trace in fig.data:
    trace.marker.line = dict(color='black')

static_trace = go.Scatter3d(
    x=df["MPG"],
    y=df["horsepower"],
    z=df["weigth"],
    mode='markers',
    marker=dict(
        size=df["cylinders"] * size_factor,
        color='gray',
        opacity=0.1
    ),
    hoverinfo="skip",
    showlegend=False
)

fig.add_trace(static_trace)

fig.show()

fig.write_html("car_data_3D_animation.html")
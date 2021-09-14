import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/finalrecycling.csv")
columns = ['name_location', 'website', 'boro', 'address_area', 'latitude', 'longitude', 'type', 'color', 'hov_txt']

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoibmd1eWVuZHVjaHV5MjcxMTk3IiwiYSI6ImNrdGlrdXR6NTEydGQyb3FmMm40M3ZzY3IifQ.2Su0FgZih2OeDc7Z4xla8g"
external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'


recycle_type_colors = html.Ul([
    html.Li("Compost", className="circle", style={'background': '#ff00ff','color':'black', 'list-style':'none','text-indent': '17px'}),
    html.Li("Electronics"),
    html.Li("Hazardous_waste"),
    html.Li("Plastic_bags"),
    html.Li("Recycling_bins"),
])


row = html.Div(
    dbc.Row(
            [
        dbc.Col(
            [
                dbc.Row(recycle_type_colors),
                dbc.Row(html.Div("One of three columns")),
                dbc.Row(html.Div("One of three columns")),
            ], width= 3
        ),
        dbc.Col(dbc.Row(html.Div("A single column")),width= 9)
    ], className="container"
    )
)



app = dash.Dash(external_stylesheets=[external_stylesheets, dbc.themes.BOOTSTRAP])

app.layout = row

if __name__ == "__main__":
       app.run_server(debug=True)

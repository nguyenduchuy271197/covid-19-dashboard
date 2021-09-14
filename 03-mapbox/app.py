import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/finalrecycling.csv")
columns = ['name_location', 'website', 'boro', 'address_area', 'latitude',
       'longitude', 'type', 'color', 'hov_txt']

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoibmd1eWVuZHVjaHV5MjcxMTk3IiwiYSI6ImNrdGlrdXR6NTEydGQyb3FmMm40M3ZzY3IifQ.2Su0FgZih2OeDc7Z4xla8g"


fig = go.Figure()

trace = go.Scattermapbox(
    data= df,
    
    )
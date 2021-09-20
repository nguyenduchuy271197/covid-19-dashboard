from logging import debug
from os import name
import os
import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

mapbox_access_token = os.environ["MAPBOX_TOKEN"]
BACKGROUND_COLOR = "#082032"
PLOT_COLOR = "#2C394B"
TEXT_COLOR = "#fff"

df = pd.read_csv("data/2011_february_us_airport_traffic.csv").dropna()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

state_dropdown = dcc.Dropdown(id="state",
                              options=[{"label": i, "value": i}
                                       for i in df["state"].unique()],
                              value="FL", placeholder="Select State")

app.layout = dbc.Row([
    dbc.Col(html.Div([
        html.H3("Aiport Traffic Data"),
        html.Div("Select State"),
        html.Div(state_dropdown)]), width=3, className="sidenav"),
    dbc.Col(html.Div([
        dcc.Graph(id="geo-graph"),
        dcc.Graph(id="arrival-bar")
    ]), width=9, style={"padding": 0})
], style={"padding": 0})


@app.callback(Output("geo-graph", "figure"), [Input("state", "value")])
def update_graph(state):
    display_df = df[df["state"] == state]
    fig = px.scatter_mapbox(
        data_frame=display_df,
        lat="lat",
        lon="long",
        color="cnt",
        custom_data=["airport", "city", "state", "cnt"],
        color_continuous_scale=px.colors.qualitative.T10_r)

    fig.update_traces(
        marker=dict(size=10),
        hovertemplate="<br>".join(["<b>State</b>: %{customdata[2]}",
                                   "<b>City</b>: %{customdata[1]}",
                                   "<b>Aiport</b>: %{customdata[0]}",
                                   "<b>Latitude</b>: %{lat}",
                                   "<b>Longitude</b>: %{lon}",
                                   "<b>Arrival</b>: %{customdata[3]}"]))
    fig.update_layout(
        mapbox=dict(accesstoken=mapbox_access_token,
                    zoom=3, style="open-street-map"),
        coloraxis_showscale=False,
        margin=dict(t=0, r=0, b=0, l=0))
    return fig


@app.callback(Output("arrival-bar", "figure"), [Input("state", "value")])
def update_graph(state):
    display_df = df[df["state"] == state]
    fig = px.bar(
        data_frame=display_df,
        x="airport",
        y="cnt",
        text="cnt",
        custom_data=["airport", "city", "state", "cnt"],
        color="cnt",
        title="Total arrival in FL state",
        color_continuous_scale=px.colors.qualitative.T10_r, height=370)

    fig.update_traces(
        textfont=dict(color=TEXT_COLOR),
        hovertemplate="<br>".join(["<b>State</b>: %{customdata[2]}",
                                   "<b>City</b>: %{customdata[1]}",
                                   "<b>Aiport</b>: %{customdata[0]}",
                                   "<b>Arrival</b>: %{customdata[3]}"]))
    fig.update_xaxes(
        showticklabels=True,
        title="",
        categoryorder="category ascending",
        ticks="outside",
        tickcolor=TEXT_COLOR)
    fig.update_yaxes(showgrid=False, showticklabels=False, title="")
    fig.update_layout(
        coloraxis_showscale=False,
        font=dict(color=TEXT_COLOR),
        paper_bgcolor=PLOT_COLOR,
        plot_bgcolor=PLOT_COLOR,
        title=dict(y=0.9),
        margin=dict(t=0, b=0))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)

import dash
from dash import html
from dash import dcc
from dash.html.Div import Div
import plotly.express as px
import pandas as pd

# Variables
options = [
    {'label': 'Action Taken by Ranger', 'value': 'Final Ranger Action'},
    {'label': 'Age', 'value': 'Age'},
    {'label': 'Animal Health', 'value': 'Animal Condition'},
    {'label': 'Borough', 'value': 'Borough'},
    {'label': 'Species', 'value': 'Animal Class'},
    {'label': 'Species Status', 'value': 'Species Status'}
]

# Read data
df = pd.read_csv("data/Urban_Park_Ranger_Animal_Condition_Response.csv")
# fig = px.pie(data_frame=df, names= options[1]["value"])
fig = px.pie(data_frame=df, names="Final Ranger Action", hole=0.3)


# Build app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children="NYC Calls for Animal Rescue"),
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value='Final Ranger Action',
        clearable=False,
        style={"width": "50%"}
    ),
    dcc.Graph(id="output", figure=fig)
])


@app.callback(
    dash.dependencies.Output('output', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    fig = px.pie(data_frame=df, names=value, hole=0.3)
    return fig


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)

import dash
from dash import html, dcc
from dash.dcc.Graph import Graph
from dash.dependencies import Input, Output
from dash.html.Div import Div
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/Urban_Park_Ranger_Animal_Condition_Response.csv")
# Drop rows w/ no animals found or calls w/ varied age groups
df = df[(df['# of Animals'] > 0) & (df['Age'] != 'Multiple')]

# Extract month from time call made to Ranger
df['Month of Initial Call'] = pd.to_datetime(
    df['Date and Time of initial call'])
df['Month of Initial Call'] = df['Month of Initial Call'].dt.strftime('%m')

# Copy columns to new columns with clearer names
df['Amount of Animals'] = df['# of Animals']
df['Time Spent on Site (hours)'] = df['Duration of Response']


app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H4("X-axis categories to compare:"),
        dcc.RadioItems(
            id= "x-axis",
            options=[
                {'label': 'Month Call Made', 'value': "Month of Initial Call"},
                {'label': 'Animal Health', 'value': "Animal Condition"},
            ],
            value="Month of Initial Call",
            labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        html.H4("Y-axis values to compare:"),
        dcc.RadioItems(
            id= "y-axis",
            options=[
                {'label': 'Time Spent on Site (hours)', 'value': 'Time Spent on Site (hours)'},
                {'label': 'Amount of Animals', 'value': "Amount of Animals"},
            ],
            value='Time Spent on Site (hours)',
            labelStyle={'display': 'inline-block'}
        )
    ]),
    dcc.Graph(id="output")
])

@app.callback(Output("output", "figure"), [Input("x-axis", "value"), Input("y-axis", "value")])
def update_graph(x, y):
    return px.bar(data_frame=df, x= x, y= y, title= f"{x}: by {y}")


if __name__ == "__main__":
    app.run_server(debug=True)

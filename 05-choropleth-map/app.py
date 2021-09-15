import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

# Read data
df = px.data.gapminder()
external_sheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


year_input = dcc.Input(id="year", value=None, placeholder="Year", type="number", debounce=True, className= "input")
button = html.Button("Submit", id="submit", n_clicks=0, className= "button")


app = dash.Dash(__name__, external_stylesheets=external_sheets)

app.layout = html.Div([
    html.Pre("Life Expectancy by Year", className="title"),
    dcc.Graph(id="output"),
    html.Div([year_input, button], style= {"margin-top": "50px"})
], style= {"text-align": "center"})


@app.callback(Output("output", "figure"), [Input("year", "value")], [State("submit", "n_clicks")])
def update_graph(year, n_clicks):
    if year is None:
        raise PreventUpdate
    else:
        fig = px.choropleth(data_frame=df.query(f"year=={year}"), 
              locations= "iso_alpha", 
              locationmode='ISO-3', 
              color= "lifeExp", 
              hover_name="continent", 
              hover_data=["pop", "gdpPercap"], 
              color_continuous_scale= "blues", 
              projection= "natural earth",
              fitbounds=False)
        fig.update_layout(clickmode="event+select", margin= dict(t=0, r=0, b=0, l=0))
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)



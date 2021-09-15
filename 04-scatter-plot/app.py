import pandas as pd
from pandas.core.algorithms import unique
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input


# Read data
df = pd.read_csv("data/suicide_rates.csv")
print(df['year'].unique())

# Create a range slider
mark_values = {1987:'1987',1988:'1988',1991:'1991',1994:'1994',
               1997:'1997',2000:'2000',2003:'2003',2006:'2006',
               2009:'2009',2012:'2012',2015:'2015',2016:'2016'}

range_slider = dcc.RangeSlider(id="range-slider", 
                                min= 1987, 
                                max= 2016, 
                                marks=mark_values, 
                                value=[1987,1992], step=None)


# Build app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1(children="Suicide Rates 1985 - 2016"),
    dcc.Graph(id="output"),
    html.Div(range_slider, style={"margin-top": "50px"})
], style= {"text-align": "center"})

@app.callback(Output("output", "figure"), [Input("range-slider", "value")])
def update_graph(interval):
    display_df = df[(df["year"] >= interval[0]) & (df["year"] <=interval[1])].groupby("country", as_index=False).mean()

    fig = px.scatter(data_frame=display_df, x= "suicides/100k pop", y= "gdp_per_capita ($)", text="country")
    fig.update_traces(textposition= "top center")
    fig.update_layout(margin= dict(t=0, r=0, b=0, l=0))
    return fig

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
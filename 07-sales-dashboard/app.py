from dash_html_components.Div import Div
from dash_html_components.H3 import H3
from dash_html_components.H4 import H4
import pandas as pd 
import plotly.express as px

import dash
# import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input



external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
             6: 'June', 7: 'July', 8: 'August', 9: 'September',10: 'October', 11: 'November', 12: 'December'}




df = pd.read_csv("./data/train.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month.map(month_dict)

{2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018'}


year_slider = dcc.Slider(
    id="year",
    min=2015,
    max=2018,
    value=2018,
    marks={2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018'},
    included=False
)

segment_radioitem = dcc.RadioItems(
    id="segment",
    options=[{"label": i, "value": i} for i in df["Segment"].unique()],
    value='Consumer',
    labelStyle={'display': 'inline-block'}
)

subcat_region_radioitem = dcc.RadioItems(
    id="subreg",
    options=[{"label": "Sub-Category", "value": "Sub-Category"}, 
             {"label": "Region", "value": "Region"}],
    value="Sub-Category",
    labelStyle={'display': 'inline-block'}
)

state_city_radioitem = dcc.RadioItems(
    id="staci",
    options=[{"label": "State", "value": "State"}, 
             {"label": "City", "value": "City"}],
    value="State",
    labelStyle={'display': 'inline-block'}
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.Div([
        html.H1("Sales Dashboard"),
        html.Div([html.H3("Year"), year_slider]),
        html.Div([html.H3("Segment"), segment_radioitem])
    ]),
    html.Div([
        html.Div([subcat_region_radioitem, dcc.Graph(id="subreg-bar")]),
        html.Div([
            html.Div("Sales by Category in year 2018"), 
            dcc.Graph(id="sales-pie")]),
        html.Div([dcc.Graph(id="sales-line")]),
        html.Div([
            html.Div([html.H3("Current Year"), html.H4("$722,052.02")]),
            html.Div([html.H3("Current Year"), html.H4("$722,052.02")]),
            html.Div([html.H3("Current Year"), html.H4("$722,052.02")])
        ])
    ]),
    html.Div([
        html.Div("A Dash Table Over Here!"),
        html.Div([state_city_radioitem, dcc.Graph(id="staci-bar")]),
        html.Div([dcc.Graph(id="sales-bubble")])
    ]),
])


@app.callback(Output("subreg-bar", "figure"), 
                [Input("year", "value"), 
                Input("segment", "value"), 
                Input("subreg", "value")])
def update_subreg_bar(year, segment, subreg):
    yr_seg_subcat_grp = df.groupby(["Year","Segment",subreg]).sum()

    five_largest_sales = yr_seg_subcat_grp.loc[(year, segment)].reset_index().nlargest(5, "Sales")
    fig = px.bar(data_frame= five_largest_sales, x="Sales", y=subreg, orientation="h")
    return fig


@app.callback(Output("sales-pie", "figure"), 
                    [Input("year", "value"), 
                    Input("segment", "value")])
def update_sales_pie(year, segment):
    sales_df = df.groupby(["Year", "Segment", "Category"]).sum().loc[(year, segment)].reset_index()
    fig = px.pie(data_frame=sales_df, names= "Category", values="Sales")
    return fig


@app.callback(Output("sales-line", "figure"), 
                    [Input("year", "value"), 
                    Input("segment", "value")])
def update_sales_pie(year, segment):
    sales_df = df.groupby(["Year", "Segment", "Month"]).sum().loc[(year, segment)].reset_index()
    fig = px.line(data_frame=sales_df, x= "Month", y="Sales")
    return fig


@app.callback(Output("staci-bar", "figure"), 
                [Input("year", "value"), 
                Input("segment", "value"), 
                Input("staci", "value")])
def update_sales_pie(year, segment, staci):
    sales_df = df.groupby(["Year", "Segment", staci]).sum().loc[(year, segment)].reset_index().nlargest(10, "Sales")
    fig = px.bar(data_frame= sales_df, x="Sales", y=staci, orientation="h")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

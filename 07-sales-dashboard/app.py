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


BACKGROUND_GRAPH_COLOR = '#30475E'

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def cvt_currency(num):
    return "${:,.2f}".format(num)

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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Sales Dashboard")
app.layout = html.Div([
    html.Div([
        html.Div(html.H1("Sales Dashboard"), style= {"width": "20%"}),
        html.Div([html.H3("Year"), year_slider], style= {"width": "50%"}),
        html.Div([html.H3("Segment"), segment_radioitem], style= {"width": "20%"})
    ], className="title-container"),
    html.Div([
        html.Div([subcat_region_radioitem, dcc.Graph(id="subreg-bar")], style= {"width": "20%"}),
        html.Div([ 
            dcc.Graph(id="sales-pie")], style= {"width": "20%"}),
        html.Div([dcc.Graph(id="sales-line")], style= {"width": "45%"}),
        html.Div([
            html.Div([html.P("Current Year"), html.P("$722,052.02")]),
            html.Div([html.P("Current Year"), html.P("$722,052.02")]),
            html.Div([html.P("Current Year"), html.P("$722,052.02")])
        ], style= {"width": "10%"})
    ], className="sales-container"),
    html.Div([
        html.Div("A Dash Table Over Here!"),
        html.Div([state_city_radioitem, dcc.Graph(id="staci-bar")]),
        html.Div([dcc.Graph(id="sales-bubble")])
    ], className="second-sales-container"),
], className="all-containers")


@app.callback(Output("subreg-bar", "figure"), 
                [Input("year", "value"), 
                Input("segment", "value"), 
                Input("subreg", "value")])
def update_subreg_bar(year, segment, subreg):
    yr_seg_subcat_grp = df.groupby(["Year","Segment",subreg]).sum()

    sales_df = yr_seg_subcat_grp.loc[(year, segment)].reset_index().nlargest(5, "Sales")
    sales_df["Format Sales"] = sales_df["Sales"].apply(human_format)
    sales_df["Currency Format"] = sales_df["Sales"].apply(lambda num: "${:,.2f}".format(num))
    fig = px.bar(data_frame= sales_df, 
                            x="Sales", 
                            y=subreg, 
                            orientation="h", 
                            text= "Format Sales", 
                            height= 400, 
                            custom_data=["Currency Format"], title= f"Sales by {subreg} {year}")
    fig.update_layout(font= dict(color= "white"), title= dict(font_size=12, x=0.5),
                                paper_bgcolor='#30475E', 
                                plot_bgcolor='#30475E',
                                yaxis=dict(autorange="reversed"), 
                                margin= dict(t=50, r=20, b=10, l=0, pad=0))
    fig.update_traces(hovertemplate="<br>".join(["Sales: %{x}", subreg + ": %{custom_data}"]))
    fig.update_xaxes(showgrid=False, showticklabels=False, title="")
    fig.update_yaxes(title="", 
                    ticklabelposition= "outside", 
                    ticks="outside", 
                    tickson="labels", 
                    ticklen=10, 
                    tickfont_color="orange", 
                    tickcolor="orange")
    return fig


@app.callback(Output("sales-pie", "figure"), 
                    [Input("year", "value"), 
                    Input("segment", "value")])
def update_sales_pie(year, segment):
    sales_df = df.groupby(["Year", "Segment", "Category"]).sum().loc[(year, segment)].reset_index()
    fig = px.pie(data_frame=sales_df, names= "Category", values="Sales", title= f"Sales by Category in year {year}", hole=0.6)
    fig.update_traces(textinfo="label+percent", textposition="outside")
    fig.update_layout(font= dict(color= "white"), paper_bgcolor=BACKGROUND_GRAPH_COLOR, plot_bgcolor=BACKGROUND_GRAPH_COLOR)
    fig.update_layout(legend=dict(x=0.25, y=-0.25, traceorder= "normal"), 
                        margin= dict(t=0, r=30, b=0, l=30), 
                        title= dict(font_size=14, x=0.5))
    return fig


@app.callback(Output("sales-line", "figure"), 
                    [Input("year", "value"), 
                    Input("segment", "value")])
def update_sales_line(year, segment):
    sales_df = df.groupby(["Year", "Segment", "Month"]).sum().loc[(year, segment)].reset_index()
    sales_df["Format Sales"] = sales_df["Sales"].apply(human_format)
    fig = px.line(data_frame=sales_df, x= "Month", y="Sales", text="Format Sales", title=f"Sales Trend in Year {year}")
    fig.update_traces(mode="markers+lines+text", textposition='bottom left', marker= dict(size=10), line_color="orange")
    fig.update_layout(font= dict(color= "white"), paper_bgcolor=BACKGROUND_GRAPH_COLOR, plot_bgcolor=BACKGROUND_GRAPH_COLOR)
    fig.update_layout(title=dict(x=0.5))
    fig.update_xaxes(showline=True, showgrid=False, title= "",
                        # ticklabelposition= "outside", 
                        ticks="outside", 
                        tickson="labels", 
                        ticklen=10, 
                        tickfont_color="orange", 
                        tickcolor="orange")
    fig.update_yaxes(showline=False, title= "", showticklabels=False)
    return fig


@app.callback(Output("staci-bar", "figure"), 
                [Input("year", "value"), 
                Input("segment", "value"), 
                Input("staci", "value")])
def update_staci_bar(year, segment, staci):
    sales_df = df.groupby(["Year", "Segment", staci]).sum().loc[(year, segment)].reset_index().nlargest(10, "Sales")
    fig = px.bar(data_frame= sales_df, x="Sales", y=staci, orientation="h")
    fig.update_layout(font= dict(color= "white"), paper_bgcolor=BACKGROUND_GRAPH_COLOR, plot_bgcolor=BACKGROUND_GRAPH_COLOR)
    return fig


# @app.callback(Output("sales-bubble", "figure"), 
#                     [Input("year", "value"), 
#                     Input("segment", "value")])
# def update_sales_bubble(year, segment):
#     sales_df = df.groupby(["Year", "Segment", "State", "City"]).sum().loc[(year, segment)].reset_index()
#     fig = px.pie(data_frame=sales_df, names= "Category", values="Sales")
#     return fig


if __name__ == "__main__":
    app.run_server(debug=True)

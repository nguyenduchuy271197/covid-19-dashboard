import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# from dash_html_components.Div import Div
import pandas as pd
# import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("data/recycling.csv")
columns = ['name_location', 'website', 'boro', 'address_area', 'latitude', 'longitude', 'type', 'color', 'hov_txt']


# Set Mapbox Access Token
MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoibmd1eWVuZHVjaHV5MjcxMTk3IiwiYSI6ImNrdGlrdXR6NTEydGQyb3FmMm40M3ZzY3IifQ.2Su0FgZih2OeDc7Z4xla8g"
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)


# Add color columns
color_dict = {"compost": "#A45D5D", 
              "electronics": "#00A19D", 
              "hazardous waste recycling": "#FEC260", 
              "plastic bag recycling": "#2D46B9", 
              "public recycling bin": "#334756"}
df['color'] = df["type"].map(color_dict)


# Visualize scatter mapbox
fig = px.scatter_mapbox(data_frame=df, 
                  lat= "latitude", 
                  lon= "longitude", 
                  color= "color", 
                  hover_name= "type", 
                  hover_data= ["boro"], 
                  opacity=1, 
                  zoom=10.5, 
                  center= dict(lat= 40.74,lon= -73.9),
                  template="plotly_dark", 
                  height=600)

fig.update_traces(selected_marker= dict(opacity= 1, size= 10), unselected_marker= dict(opacity= 0.6))

fig.update_layout(margin= dict(t=0, l=0, b=0, r=0), 
                  showlegend= False, 
                  mapbox=dict(bearing=20,pitch=40), 
                  clickmode= "event+select")


legend = html.Div([
    html.Div("Explanation of Scattermapbox", className="legend-title"),
    html.Div([
        html.Ul([
            html.Li(["Compost", html.Span(style={"background-color": color_dict["compost"]})]),
            html.Li(["Electronics", html.Span(style={"background-color": color_dict["electronics"]})]),
            html.Li(["Hazardous Waste Recycling", html.Span(style={"background-color": color_dict["hazardous waste recycling"]})]),
            html.Li(["Plastic Bag Recycling", html.Span(style={"background-color": color_dict["plastic bag recycling"]})]),
            html.Li(["Public Recycling Bin", html.Span(style={"background-color": color_dict["public recycling bin"]})])
        ], className="legend-labels")
    ], className="legend-scale")
])


boro_checklist = html.Div([
    html.Div("Borough:", className="legend-title"),
    dcc.Checklist(
    id="boro-checklist",
    options=[{"label": i, "value": i} for i in df["boro"].unique()],
    value=df["boro"].unique(),
    labelStyle={"display": "block"}
)
])

type_checklist = html.Div([
    html.Div("Recycle Types:", className="legend-title"),
    dcc.Checklist(
    id="type-checklist",
    options=[{"label": i, "value": i} for i in df["type"].unique()],
    value=df["type"].unique(),
    labelStyle={"display": "block"}
)
])

website = html.Div([
    html.Div("Website:", className="legend-title"),
    html.Pre(children= "asdasd", id="website", style= {"border": "1px solid black", 
                                                        "text-align": "center", 
                                                        "padding": "10px", 
                                                        'white-space': 'pre-wrap', 
                                                        'word-break': 'break-all'})
])

list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem(legend),
        dbc.ListGroupItem(boro_checklist),
        dbc.ListGroupItem(type_checklist),
        dbc.ListGroupItem(website)
    ]
)


row = dbc.Row([
    dbc.Col(list_group, width= 3),
    dbc.Col([
        html.H1("Where to Recycle?"),
        dcc.Graph(id="graph-output")], width=9, className="graph")
])



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = row

@app.callback(Output("graph-output", "figure"),[Input("boro-checklist", "value"), Input("type-checklist", "value")])
def update_figure(boro, types):
    print(boro)
    display_df = df[(df["boro"].isin(boro)) & (df["type"].isin(types))]
    print(types)
    print()
    fig = px.scatter_mapbox(data_frame=display_df, 
                  lat= "latitude", 
                  lon= "longitude", 
                  color= "color", 
                  hover_name= "type", 
                  hover_data= ["boro", "website"],
                  custom_data=["website"],
                  opacity=1, 
                  zoom=10.5, 
                  center= dict(lat= 40.74,lon= -73.9),
                  template="plotly_dark", 
                  height=650, width=1000)

    fig.update_traces(selected_marker= dict(opacity= 1, size= 10), unselected_marker= dict(opacity= 0.6))

    fig.update_layout(margin= dict(t=0, l=0, b=0, r=0), 
                    showlegend= False, 
                    mapbox=dict(bearing=20,pitch=40), 
                    clickmode= "event+select")
    return fig
    
@app.callback(Output("website", "children"), [Input("graph-output", "clickData")])
def update_website(click_data):
    if click_data is None:
        return "Click a point on map"
    else:
        print(click_data)
        output = click_data["points"][0]["customdata"][0]
        print(output)
        if "http" not in output and output is None:
            return "No web here!"
        return html.A(children=output, href=output)

if __name__ == "__main__":
       app.run_server(debug=True)

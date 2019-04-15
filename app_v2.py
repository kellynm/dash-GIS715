import pandas as pd
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output

# API keys and datasets
mapbox_access_token = 'pk.eyJ1Ijoia2VsbHlubSIsImEiOiJjanM0eDF0ZngwMjZ0M3lwYjV5MWxqZm1xIn0.49GaijkpupewHcHf2niUDA'
df = pd.read_csv('data/ca_fires.csv')

# Select only required columns
map_data = df[["fire_name", "fire_year", "date", "fire_size", "latitude", "longitude", "cause", "duration_days"]].drop_duplicates()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'California Wildfires' # This is what shows up as the browser tab name

app.layout = html.Div([
    html.Div([
        html.H1("California Wildfires (1992-2015)")
    ], style={
        'textAlign': "center",
        "padding-bottom": "10",
        "padding-top": "10"}),
    html.Div([
        dcc.Dropdown(id="cause-selected",
                     options=[
                         {'label': str(item),
                        'value': str(item)} for item in set(map_data['cause'])
                        ],
                     value=map_data.cause.unique(),
                     multi=True,
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "50%"

                    }
        )
    ]),
    html.Div([
        dcc.Slider(id="year-slider",
                    min=map_data['fire_year'].min(),
                    max=map_data['fire_year'].max(),
                    value=map_data['fire_year'].min(),
                    marks={str(fire_year): str(fire_year) for fire_year in map_data['fire_year'].unique()}
        )
    ]),
    html.Div(dcc.Graph(id="my-graph"))
],className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("cause-selected", "value"),
    dash.dependencies.Input("year-slider", "value")]

)
def update_figure(selected):
    trace = []
    for year in selected:
        dff = map_data[map_data["fire_year"] == year]
        trace.append(go.Scattermapbox(
            lat=dff["latitude"],
            lon=dff["longitude"],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            ),
            text=[["Name: {} <br>Date: {} <br>Duration: {} <br>Cause: {}".format(i,j,k,l)]
                                for i,j,k,l in zip(dff['fire_name'], dff['date'], dff['duration_days'], dff['cause'])],
            hoverinfo='text',
            name=year
        ))
    return {
        "data": trace,
        "layout": go.Layout(
            autosize=True,
            hovermode='closest',
            showlegend=False,
            height=700,
            mapbox={'accesstoken': mapbox_access_token,
                    'bearing': 0,
                    'center': {'lat': 37.037921, 'lon': -120.061779},
                    'pitch': 30, 'zoom': 5,
                    "style": 'mapbox://styles/mapbox/light-v9'},
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

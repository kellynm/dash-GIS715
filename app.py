import os

import pandas as pd
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output

#os.chdir("data")

# API keys and datasets
mapbox_access_token = 'pk.eyJ1Ijoia2VsbHlubSIsImEiOiJjanM0eDF0ZngwMjZ0M3lwYjV5MWxqZm1xIn0.49GaijkpupewHcHf2niUDA'
df = pd.read_csv('data/ca_fires.csv')

# Select only required columns
map_data = df[["fire_name", "fire_year", "date", "fire_size", "latitude", "longitude", "cause", "duration_days"]].drop_duplicates()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app = dash.Dash(__name__)
app.title = 'California Wildfires' # This is what shows up as the browser tab name


markdown_text = '''
### Dash and Markdown
A lot of text
'''

#  Layouts
'''layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)'''

'''layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='California Wildfires',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-120.061779,
            lat=37.037921
        ),
        zoom=7,
    )
)

# functions
def gen_map(map_data):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(map_data['latitude']),
                "lon": list(map_data['longitude']),
                "hoverinfo": "text",
                "hovertext": [["Name: {} <br>Date: {} <br>Duration: {} <br>Cause: {}".format(i,j,k,l)]
                                for i,j,k,l in zip(map_data['fire_name'], map_data['date'],map_data['duration_days'],map_data['cause'])],
                "mode": "markers",
                "name": list(map_data['fire_name']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }'''

app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='California Wildfires (1990-2015)',
                        className='nine columns'),
                html.Div(className='three columns'),
                
                html.H2(children='''
                        GIS 714 - Dash Lab
                        ''',
                        className='nine columns'
                ),
                
            ], className="row"
        ),

        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Cause of Fire:'),
                        dcc.Checklist(
                                id = 'cause',
                                options=[
                                    {'label': 'Human', 'value': 'Human'},
                                    {'label': 'Natural', 'value': 'Natural'},
                                    {'label': 'Unknown', 'value': 'Unknown'},
                                ],
                                values=['Human', 'Natural', "Unknown"],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Year(s):'),
                        dcc.Dropdown(
                            id='year',
                            options= [{'label': str(item),
                                                  'value': str(item)}
                                                 for item in set(map_data['fire_year'])],
                            multi=True,
                            value=list(set(map_data['fire_year']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dt.DataTable(
                            data=map_data.to_dict('rows'),
                            columns=map_data.columns,
                            row_selectable=True,
                            filtering=True,
                            sorting=True,
                            selected_rows=[],
                            id='datatable'),
                    ],
                    #style = layout_table,
                    className="twelve columns"
                ),
                '''html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),'''
                html.Div([
                        dcc.Graph(
                            id='bubble'
                        )
                    ], className= 'six columns'
                    ),
            ], className="row"
        )
    ], className='ten columns offset-by-one'))


'''@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'data')])
def map_selection(data):
    aux = pd.DataFrame(data)
    return gen_map(aux)'''

@app.callback(
    Output('datatable', 'data'),
    [Input('cause', 'values'),
     Input('year', 'value')])
def update_selected_rows(cause, year):
    map_aux = map_data.copy()

    # Cause filter
    map_aux = map_aux[map_aux['cause'].isin(cause)]
    # Year filter
    map_aux = map_aux[map_aux["fire_year"].isin(year)]

    data = map_aux.to_dict('rows')
    return data

@app.callback(
    Output('bubble', 'figure'),
    [Input('datatable', 'data')])
def update_figure(data):
    dff = pd.DataFrame(data)

    traces = []
    for i in dff.cause.unique():
        df_by_cause = dff[dff['cause']==i]
        traces.append(go.Scatter(
            x=df_by_cause['date'],
            y=df_by_cause['fire_year'],
            text=df_by_cause['fire_name'],
            mode='markers',
            opacity = 0.7,
            marker={
                'size':dff['fire_size'],
                'sizemode':'area',
                'sizeref':2.*max(dff['fire_size'])/(40.**2),
                'sizemin':4
            },
            name=i
        ))
    
    return{
        'data':traces,
        'layout': go.Layout(
            xaxis={'title': 'date'},
            yaxis={'title': 'year'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'California Wildfires' # This is what shows up as the browser tab name

df = pd.read_csv('data/ca_fires.csv')
# Select only required columns
df = df[["fire_name", "fire_year", "plot_date", "fire_size", "latitude", "longitude", "cause", "duration_days"]].drop_duplicates()


trace1 = go.Bar(x=df[df['cause']=='Human']['fire_year'], y=df[df['cause']=='Human']['fire_size'], 
    transforms = [dict(
    type = 'aggregate',
    aggregations = [dict(
    target = 'y', func = 'sum', enabled = True)
    ])], name='Human')
#trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
#trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')

app.layout = html.Div(children=[
    html.H1(children='California Wildfires'),

    html.H2(children='''
        1993-2015
    '''),
    dcc.Graph(
        id='bar-graph',
        figure={
            'data': [
                trace1
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
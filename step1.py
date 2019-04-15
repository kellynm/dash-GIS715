import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'California Wildfires' # This is what shows up as the browser tab name

df = pd.read_csv('data/ca_fires.csv')

app.layout = html.Div([
    dcc.Graph(
        id='bubble',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['cause'] == i]['date'],
                    y=df[df['cause'] == i]['fire_year'],
                    text=df[df['cause'] == i]['fire_name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                            'size': df[df['fire_size']],
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df.cause.unique()
                    # print(df.cause.unique())
               ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Year'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
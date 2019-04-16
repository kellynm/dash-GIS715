# step4_linkGraphs.py
# GIS 715 Student-led lab - Dash
# Use range slider to filter map data as well.

# Now we will use the range slider to filter the data plotted in the map as well. Just like before, we will add another callback
# that takes the range slider years as input and outputs an updated map. We need to remove the map graph element from the main Dash layout.

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'California Wildfires'

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

df = pd.read_csv('data/ca_fires.csv')
df.duration_days = df.duration_days.fillna(0.0).astype(int)

# Mapbox API key
# Be sure to replace the key below with yours.
mapbox_access_token = 'pk.eyJ1Ijoia2VsbHlubSIsImEiOiJjanM0eDF0ZngwMjZ0M3lwYjV5MWxqZm1xIn0.49GaijkpupewHcHf2niUDA'

# Set up layout for map
layout_map = dict(
    autosize=True,
    height=525,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=15
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=12), orientation='h'),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-120.061779,
            lat=37.037921
        ),
        zoom=5,
    )
)

app.layout = html.Div(children=[
    html.H1(
        children='California Wildfires',
        style={
            'textAlign': 'center'
        }
    ),

    html.H3(
        children='''1992-2015''',
         style={
            'textAlign': 'center'
        }
    ),
    html.H5(
        children='''1,000 ac or larger''',
         style={
            'textAlign': 'center'
        }
    ),
     html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='map-with-slider',  # Make sure this map id matches the output id in the callback for updating the map
                        style={'margin-top': '25'}
                    ),
                ], className = 'five columns'
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='bubble-with-slider'
                    ),
                    dcc.RangeSlider(
                        id='range-slider',
                        min=df['fire_year'].min(),
                        max=df['fire_year'].max(),
                        value=[df['fire_year'].min(),df['fire_year'].max()],
                        marks={str(year): str(year) for year in df['fire_year'].unique()}
                    )
                ], className = 'seven columns'
        ),
            html.Div(
                [
                    html.P('Created by Kellyn Montgomery for GIS 715 Geovisualization Student-led Lab, Spring 2018', style = {'display': 'inline'})
                ], className = "twelve columns",
                    style = {'fontSize': 18, 'padding-top': 20}
            ),
            html.Div(
                [
                    html.P('Data from https://github.com/BuzzFeedNews/2018-07-wildfire-trends', style = {'display': 'inline'})
                ], className = "twelve columns",
                    style = {'fontSize': 18, 'padding-top': 20}
            )
        ], className ="row"
     )
])

@app.callback(
    Output('map-with-slider', 'figure'), # Output specifies the id of the graph object in the main Dash layout that will be updated with this callback
    [Input('range-slider', 'value')]) # Input are min and mix values for range of years selected in range slider above 

def update_map(selected_range):
    start = selected_range[0]
    end = selected_range[1]
    year_list = list(range(start, end+1))
    filtered_df = pd.DataFrame()
    for year in year_list:
        new_df=df[df.fire_year == year]
        filtered_df = filtered_df.append(new_df)
    filtered_data = [
        go.Scattermapbox( # Create map with dataframe filtered by range slider years.
            lat= list(filtered_df[filtered_df['cause'] == i]['latitude']),
            lon= list(filtered_df[filtered_df['cause'] == i]['longitude']),
            text=["Name: {} <br>Date: {} <br>Duration (days): {} <br>Cause: {}".format(i,j,k,l) for i,j,k,l in 
                zip(filtered_df[filtered_df['cause'] == i]['fire_name'], filtered_df[filtered_df['cause'] == i]['date'], 
                filtered_df[filtered_df['cause'] == i]['duration_days'], filtered_df[filtered_df['cause'] == i]['cause'])],
            hoverinfo='text',
            mode= "markers",
            marker= {
                "size": 6,
                "opacity": 0.7
            },
            name=i
            ) for i in filtered_df.cause.unique()
        ]

    return {
        'data': filtered_data,
        "layout": layout_map
    }


@app.callback(
    Output('bubble-with-slider', 'figure'),
    [Input('range-slider', 'value')])

def update_figure(selected_range):
    start = selected_range[0]
    end = selected_range[1]
    year_list = list(range(start, end+1))
    filtered_df = pd.DataFrame()
    for year in year_list:
        new_df=df[df.fire_year == year]
        filtered_df = filtered_df.append(new_df)
    filtered_data = [
        go.Scatter(
            x=filtered_df[filtered_df['cause'] == i]['plot_date'],
            y=filtered_df[filtered_df['cause'] == i]['fire_year'],
            text=["Name: {} <br>Date: {} <br>Duration (days): {} <br>Cause: {}".format(i,j,k,l) for i,j,k,l in 
                zip(filtered_df[filtered_df['cause'] == i]['fire_name'], filtered_df[filtered_df['cause'] == i]['date'], 
                filtered_df[filtered_df['cause'] == i]['duration_days'], filtered_df[filtered_df['cause'] == i]['cause'])],
            hoverinfo='text',
            mode='markers',
            opacity=0.7,
            marker={
                    'size':filtered_df['fire_size'],
                    'sizemode':'area',
                    'sizeref':2.*max(df['fire_size'])/(40.**2),
                    'sizemin':4,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in filtered_df.cause.unique()
        ]

    return {
        'data': filtered_data,
        'layout': go.Layout(
                xaxis={'title': 'Date',
                       'tickvals': ['2017-01-01', '2017-03-01', '2017-05-01', '2017-07-01', '2017-09-01', '2017-11-01', '2018-01-01'],
                       'ticktext': ['Jan', 'Mar', 'May', 'Jul', 'Sept', 'Nov', 'Jan']},
                yaxis={'title': 'Year'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',   
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
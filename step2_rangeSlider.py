# step2_rangeSlider.py
# GIS 715 Student-led lab - Dash
# Add range slide to interactively select range of years for filtering date and update bubble chart. 

# To add any interactive elements (beyond what comes out of the box), like check boxes, drop drow select, or sliders,
# you have to add a callback which takes an input core component (a range slider in this case) and outputs another 
# core component (a graph using the filtered data in this case). When the interactive event fires (moving the slider),
# the callback is triggered which executes a function that will execute the desired response action (updating graph in this case).
# Whenever you add a callback that will result in an updated graph, you must remove the code in the main Dash layout
# element for the original, static graph.

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'California Wildfires'

df = pd.read_csv('data/ca_fires.csv')
df.duration_days = df.duration_days.fillna(0.0).astype(int)

app.layout = html.Div(children=[
    html.H1(children='California Wildfires'),

    html.H2(children='''
        1992-2015
    '''),
    html.H5(
        children='''1,000 ac or larger''',
         style={
            'textAlign': 'center'
        }
    ),
    dcc.Graph(
        id='bubble-with-slider'), # Removed original, static code for the bubble graph. Keep graph id and make sure it matched the output of the callback below.
    dcc.RangeSlider( # Add Range Slider core component to display below bubble graph.
        id='range-slider',
        min=df['fire_year'].min(),
        max=df['fire_year'].max(),
        value=[df['fire_year'].min(),df['fire_year'].max()], # Specify desired starting values - all years in this case
        marks={str(year): str(year) for year in df['fire_year'].unique()}
    )
])


@app.callback(
    Output('bubble-with-slider', 'figure'), # Output will be bubble graph component in main Dash layout above
    [Input('range-slider', 'value')]) # Input are min and mix values for range of years selected in range slider above

def update_figure(selected_range): # Here you define what should happen when callback is triggered.
    start = selected_range[0]
    end = selected_range[1]
    year_list = list(range(start, end+1)) # Get full list of years in selected range
    filtered_df = pd.DataFrame() # Create empty dataframe
    for year in year_list:
        new_df=df[df.fire_year == year]
        filtered_df = filtered_df.append(new_df) # Append records for each year in list to the empty dataframe above. This will hold the filtered values to use for the updated graph
    filtered_data = [
        go.Scatter( # Create new scatter plotly object with filtered data
            x=filtered_df[filtered_df['cause'] == i]['plot_date'],
            y=filtered_df[filtered_df['cause'] == i]['fire_year'],
            text=["Name: {} <br>Date: {} <br>Duration (days): {} <br>Cause: {}".format(i,j,k,l) for i,j,k,l in zip(filtered_df[filtered_df['cause'] == i]['fire_name'], 
                        filtered_df[filtered_df['cause'] == i]['date'], filtered_df[filtered_df['cause'] == i]['duration_days'], filtered_df[filtered_df['cause'] == i]['cause'])],
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

    return { # Returns the data and layout elements formatted as needed for main Dash layout above
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
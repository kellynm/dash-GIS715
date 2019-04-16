# step1_bubble.py
# GIS 715 Student-led lab - Dash
# Create app with bubble chart of California fires by cause. 

# To start, we will just recreate the bubble chart from the ggplotly lab and display it with the default plotly functionality. 

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__) # Initialize a Dash app object
app.title = 'California Wildfires' # This is what shows up as the browser tab name

df = pd.read_csv('data/ca_fires.csv') # Use pandas (Python's data science package which uses dataframes) to read the California fires data
df.duration_days = df.duration_days.fillna(0.0).astype(int) # Change duration to integer for prettier printing. This also changes any missing values to 0, which is not the best solution...

# Notice there is only one main Dash layout object in this script. 
# It sets the layout and specifies what data visualizations will be included. It is made up of dash html components and dash core components.
# You can include as many core components (graphs, tables, interactive elements) as you want, but each must have a unique id name.
app.layout = html.Div(children=[
    html.H1(children='California Wildfires'), # Title

    html.H2(children='''
        1992-2015
    '''),
    html.H5(
        children='''1,000 ac or larger''',
         style={
            'textAlign': 'center'
        }
    ), # Subtitle   
    dcc.Graph( # A graph component. It must have an id and figure elements. And the figure element must have data and layout elements. This graph is very similar to the ggplotly bubble graph we made earlier this week.
        id='bubble',
        figure={
            'data': [
                go.Scatter( # Here is the call to the Plotly graph_objs library. Plotly has great documentation for all of the graph parameters you can use to customize and add functionality.
                    x=df[df['cause'] == i]['plot_date'],
                    y=df[df['cause'] == i]['fire_year'],
                    text=["Name: {} <br>Date: {} <br>Duration (days): {} <br>Cause: {}".format(i,j,k,l) for i,j,k,l in zip(df[df['cause'] == i]['fire_name'], df[df['cause'] == i]['date'], df[df['cause'] == i]['duration_days'], df[df['cause'] == i]['cause'])],
                    hoverinfo='text',
                    mode='markers',
                    opacity=0.7,
                    marker={
                            'size':df['fire_size'],
                            'sizemode':'area',
                            'sizeref':2.*max(df['fire_size'])/(40.**2),
                            'sizemin':4,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df.cause.unique() # Using a FOR loop to plot fires from each cause category (Human, Natural, Unknown) separately so the fires points will be colored by cause.
               ],
            'layout': go.Layout( # Customize the graph layout
                xaxis={'title': 'Date',
                       'tickvals': ['2017-01-01', '2017-03-01', '2017-05-01', '2017-07-01', '2017-09-01', '2017-11-01', '2018-01-01'],
                       'ticktext': ['Jan', 'Mar', 'May', 'Jul', 'Sept', 'Nov', 'Jan']},
                yaxis={'title': 'Year'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
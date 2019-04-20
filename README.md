# Dash by Plotly
 ### GIS 714 Geovisualization Spring 2019 - Student-led lab

Dash is a Python framework for building interactive web applications for data visualization. Dash is rendered in a browser and uses CSS, so it is highly customizable and easy to share via URLs. Dash uses purely Python with html components and Plot.ly graph objects.

This tutorial will demonstrate how to create a basic dashboard application showing a bubble chart, map, and interactive filtering with a range slider. The tutorial will add elements step-by-step to demonstrate how to iteratively add functionality to a dashboard. 

This tutorial uses data on California wildfires larger than 1,000 acres from 1992-2015. The original data [linked here](https://github.com/BuzzFeedNews/2018-07-wildfire-trends) was posted by Buzz Feed News.

## 1. Install Dash and Plotly
* Open <i>Visual Studio Code</i>
* Click <b>Terminal</b> from the top menu and select <b>New Terminal</b>.
* In terminal, run:
```
pip install dash
pip install plotly --upgrade
pip install --upgrade pandas
```
## 2. Install Python Extension for VS Code
* In <i>Visual Studio Code</i>, press <b> Crtl + Shift + X</b> to open the list of available Extensions.
* Search for Python and click <b>Install</b>.

## 3. Download data and scripts
1. If you haven't already done so, go to https://github.com/kellynm/dash-GIS715 and download the tutorial repository. (Select <b>Clone or Download</b> from the main repo page and download zip.) Alternatively, if you have Git set up on you computer and would prefer to use the command line, follow the bulleted steps below instead of downloading the zip:
* Select <b>Clone or Download</b> and copy the repository web URL (https://github.com/kellynm/dash-GIS715.git).
* In a terminal, navigate to the directory where you'd like to save the repository.
* In terminal, run:
```
git clone https://github.com/kellynm/dash-GIS715.git
```

2. In <i>Visual Studio Code</i>, select <b>File</b>, <b>Open folder</b>, and browse to the <b>dash-715</b> folder.

## 4. Run first Dash script to create bubble chart

1. Select <b>step1_bubble.py</b> in the Explorer panel to view the first script.

This script will create and run a Dash application containing a bubble chart of the California wildfire similar to the one we created in ggplotly. Read the comments for more details about the code structure. <br>

Notice there is only one main Dash layout object in this script. It sets the layout and specifies what data visualizations will be included. It is made up of dash html components and dash core components. You can include as many core components (graphs, tables, interactive elements) as you want, but each must have a unique id name.

2. Double check you are in the <b>dash-715</b> folder in the terminal. Right click anywhere in the script or on the script file name in the Explorer panel and select <b>Run Python File in Terminal</b>.

This will execute the code and run the app on localhost server.

3. In the terminal output, an IP address will be listed (http://127.0.0.1:8050/). <b>Ctrl + click</b> the address to open the app in a browser. Use <b>Crtl + C</b> to terminate the server if needed.

## 5. Run second Dash script to add range slider

1. Select <b>step2_rangeSlider.py</b> in the Explorer panel to view the second script.

This script will add an interactive range slider to filter the data by years. Read the comments for more details about the code structure. <br>

To add interactive elements, like check boxes, drop down selection, or sliders, you have to add a callback which takes an input core component (a range slider in this case) and outputs another core component (a graph using the filtered data in this case). 

When the interactive event fires (moving the slider in this case), the callback is triggered, which executes a function that will execute the desired response action (updating graph in this case). 

Whenever you add a callback that will result in an updated graph, you must remove the code for the original, static graph in the main Dash layout (app.layout).

1. Right click anywhere in the script or on the script file name in the Explorer panel and select <b>Run Python File in Terminal</b>.

This will execute the code and run the app on localhost server.

3. In the terminal output, an IP address will be listed (http://127.0.0.1:8050/). <b>Ctrl + click</b> the address to open the app in a browser. Use <b>Crtl + C</b> to terminate the server if needed.

## 6. Run third Dash script to add a map

1. Select <b>step3_map.py</b> in the Explorer panel to view the third script.

This script will add a map of the fire locations colored by cause. Read the comments for more details about the code structure.

Now we will add a second component to the Dash layout. We can use the scattermapbox plotly object to create a map of fire point locations. For now the map is not interactive (beyond the out of the box functionality). We will use a style sheet (CSS) to place the components within the layout into rows and columns.

2. On line 28 of the script, insert your Mapbox token.

3. Right click anywhere in the script or on the script file name in the Explorer panel and select <b>Run Python File in Terminal</b>.

This will execute the code and run the app on localhost server.

3. In the terminal output, an IP address will be listed (http://127.0.0.1:8050/). <b>Ctrl + click</b> the address to open the app in a browser. Use <b>Crtl + C</b> to terminate the server if needed.

## 7. Run final Dash script to use the range slider to filter the map

1. Select <b>step4_linkGraphs.py</b> in the Explorer panel to view the fourth script.

This script will add another callback to use the range slider to filter the map data as well. Read the comments for more details about the code structure.

Just like before, we will add a callback that takes the range slider years as input and outputs an updated map. Again, we need to remove the map graph element from the main Dash layout.

2. On line 27 of the script, insert your Mapbox token.

3. Right click anywhere in the script or on the script file name in the Explorer panel and select <b>Run Python File in Terminal</b>.

This will execute the code and run the app on localhost server.

3. In the terminal output, an IP address will be listed (http://127.0.0.1:8050/). <b>Ctrl + click</b> the address to open the app in a browser. Use <b>Crtl + C</b> to terminate the server if needed.

## 8. Add a data table component

1. Try adding a data table component below the map and bubble plot. You'll need to import the dash_table library.

```python
import dash_table as dt

html.Div(
    [
        dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows"),
            style_table={'overflowX': 'scroll'}
        )]
```
2. Try another approach for adding data table using a function instead of dash_table library

```python
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

html.H4(children='California Wildfires'), 
generate_table(df)
```

## Resources

* [Announcement of Dash release with high level description.](https://medium.com/@plotlygraphs/introducing-dash-5ecf7191b503)
* [Dash Getting Started tutorial.](https://dash.plot.ly/getting-started)
* [Helpful tutorial by Adriano Yoshino with videos.](https://github.com/amyoshino/Dash_Tutorial_Series) 
  <i>Note that some functionality shown in this tutorial is now deprecated, but updates can easily be found in Dash documentation.</i>
* [Plot.ly documentation.](https://plot.ly/python/reference/)
* [Collection of Dash resources including tutorials.](https://github.com/ucg8j/awesome-dash)

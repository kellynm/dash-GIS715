# Dash by Plotly
 GIS 714 Geovisualization Spring 2019 - Student-led lab

## 1. Install Dash and Plotly
* Open Visual Studio Code and open new terminal.<br>
* Run: <br>
```
pip install dash
pip install plotly --upgrade
pip install --upgrade pandas
```

## 2. Set up Visual Studio
1. Open folder of Git repository containing python scripts and data
>* Click <b>Components</b> link from the left pane and look through the available components.
>* Click <b>Utilities</b> link and do the same for the available Utilities.

2. Go to the <b>Example</b> link in the header and click <b>Blog</b>.  We will be using modified version of this <b>Blog</b> example as a template. Download and unzip the zipfile for this repository if you haven't already done so (Select "Clone or Download" from the main repo page). A slightly modified version of the Blog template is included in the zipfile.

3. We will be using the local server you created in <b>webdev-01</b> lab.
>* Open <i>Visual Studio Code</i> and click <b>File</b> > <b>Open Folder</b> and browse to the <b>geovis-spring-2019</b> folder.
>* Click <b>Terminal</b> from the top menu and select <b>New Terminal</b>.
>* Run Node local server ( This should just be <b>node app.js</b>, Open the web browser and browse to localhost:9000/index.html link. If this does work return to the instructions in <i>webdev-01 6.10</i>).

4. The <b>webdev-02</b> folder (from the downloaded zipfile) contains a <i>vender</i> folder and some <i>html</i> files.  Copy them to <b>public</b> folder of your current project.

5. Create <i>css</i>, <i>js</i>, and <i>imgs</i> folders in <b>public</b> folder (see directory tree below).<br>

    ├── css<br>
    ├── imgs<br>
    ├── js<br>
    └── vender<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── css<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── js<br>

6. Terminate Node server in order to apply updates (<i>webdev-01 6.12</i>).

7. Reflesh browser to see the updates (you should see similar to <b>Blog</b> example).


## 3. Install nodemon

1. Go to [nodemon] nodemon is a tool that helps develop node.js based applications by automatically restarting the node application when file changes in the directory are detected.(Learn more about it here: https://www.npmjs.com/package/nodemon).

2. In the terminal,<br>
```npm install -g nodemon```


## Update Blog template

1. Change font
    * Find font from [Google Fonts](https://fonts.google.com/) and apply it to your <i>index.html</i>.  You can use original font if you prefer, but try changing the font at least once. To do so, in <i>index.html</i>, look for the following code and replace <i>Playfair</i> with the font name of your choosing: <br> 
<b>&lt;link href="https://fonts.googleapis.com/css?family=Playfair+Display:700,900" rel="stylesheet"&gt;</b>
<br>For more about changing fonts see https://developers.google.com/fonts/docs/getting_started

2. Change image
    * Create a new folder in <i>public</i> folder and name it <b>imgs</b>.
    * Find an image to replace the gray background (on the top of the <i><b>Spring 2019</b></i> page) and save it in <i>imgs</i> folder.  If you are downloading image from online, make sure you find a royalty free image.
    * Change the image url in 
``` css
background-image: url("./imgs/your_image_file");
```
    * Reflesh your browser to see the results.

3. Create CSS file for your web page.
    * Create <b>style.css</b> file in <i>css</i> folder.
    * Copy the contents of <b>&lt;style&gt;</b> tag to <i>style.css</i> and save the file. Be sure NOT to include the script opening and closing tags in what you copy to the style sheet. (In other words, don't include &lt;style&gt; and &lt;/style&gt;)
    * Modify the image path to reflect the new relative position. Now the style.css file that's refering to the image is in the css subdirectory, so instead of a single dot, you'll need double dot to step up a directory, something like this:  "../imgs/MyFabulousImage.jpg"  (instead of "./imgs/MyFabulousImage.jpg")
    * Delete the styling code from <i>index.html</i> and save the file.
    * Reflesh the browser.

4. Change the text on the image.

5. Modify <b>About</b> on the right side of the page.

6. Add a GeoVis course link in the <b>Elsewhere</b> section.

7. Add favicon
    * Find the <b>favicon.ico</b> file in the <i>webdev-02/imgs</i> folder and copy it to your <i>imgs</i> folder.
    * Reflesh the browser and you should see the red icon in the tab.

8. Creating JavaScript file for <i>dashboard.html</i> file.
    * Create a <i>dashboard.js</i> file in the <i>js</i> folder.
    * Copy the very last JavaScript code to <i>dashboard.js</i> and save the file.
    * Reference <i>dashboard.js</i> file in <i>dashboard.html</i> file.

9. Reflesh browser and click on the Dashboard link in the upper right-hand corner of the page to see your dashboard.
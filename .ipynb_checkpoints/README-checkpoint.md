# Mission to Mars

![mission_to_mars](Images/results1.png)

This assignment was to build an application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The work was completed in two steps:   Scraping 5 websites, then adding the data to a mongoDatabase and building a website to display only the scraped results.    The user can initiate a new scrape at anytime.


## Tool & Technologies Used: 

Step1: Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
Step2: MongoDB with Flask templating to create a new HTML page
 

## Step 1 - Scraping

#### NASA Mars News

* Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assigned the text to variables which were later referenced.


#### JPL Mars Space Images - Featured Image

* Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Use splinter to navigate the site and found the complete URL for the featured image.  The URL was saved as a variable and referenced later.

#### Mars Weather

* Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scraped the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable to be referenced later.

#### Mars Facts

* Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Using Pandas, the data was converted to an HTML table string.

#### Mars Hemispheres

* Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.   The URL for each hemisphere was stored in a library as (you guessed it!) a variable to be refrenced later.

## Step 2 - MongoDB and Flask Application

Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Converted the Jupyter notebook into a Python script.  All of the scraping code from above was returned in one Python dictionary.

* Created a route called `/scrape` that imports the precious script to call all the scrape functions. 

* Scraped data is stored in a Mongo database as a Python dictionary.

* Created a root route `/` which queried the Mongo database and then passed the scraped data into an HTML template which displayed the data.

* Finally, created an `index.html` which displayed the data.   The user has a button where they can scrape the latest results at any time.

## To Execute
<br>Download the files.   Ensure the correct chromedriver file is included.   (NOTE:  only applies to Windows.  MAC users will have a different file.)
<br>From the same directory as app.py, execute the following command:     python app.py
<br>The command line will indicate the location of the webpage.  Likely, http://127.0.0.1:5000/

# Screen Images

![mission_to_mars](Images/results1.png)
<br>
![mission_to_mars](Images/results2.png)
<br>
![mission_to_mars](Images/results3.png)
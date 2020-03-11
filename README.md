# Data Science Activity: Web Scraping - Mission to Mars

Built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Step 1 - Scraping

Completed the initial scraping and analysis tasks using [this Jupyter Notebook](https://github.com/anulkar/web-scraping-challenge/blob/master/Missions_to_Mars/mission_to_mars.ipynb), along with BeautifulSoup, Pandas, and Splinter.

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text/Teaser.

### JPL Mars Space Images - Featured Image

* Visited the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
* Used splinter to navigate the site and find the full size .jpg image url for the current Featured Mars Image.

### Mars Weather

* Visited the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scraped the latest Mars weather tweet from the page.

### Mars Facts

* Visited the Mars Facts webpage [here](https://space-facts.com/mars/) and used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

### Mars Hemispheres

* Visited the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mars' hemispheres.

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create an HTML page that displays all of the information that was scraped from the URLs above.

* Started by converting the Jupyter notebook into [a Python script](https://github.com/anulkar/web-scraping-challenge/blob/master/Missions_to_Mars/scrape_mars.py) with a function called `scrape` that executes all of the scraping code from the Jupyter Notebook and returns one Python dictionary containing all of the scraped data.

* Created [a Flask app](https://github.com/anulkar/web-scraping-challenge/blob/master/Missions_to_Mars/app.py) with a route called `/scrape` that imports the `scrape_mars.py` script and calls the `scrape` function.

* Created a root route `/` that queries Mongo database and passes the mars data into an HTML template to display the data.

* Created a template HTML file called [`index.html`]((https://github.com/anulkar/web-scraping-challenge/blob/master/Missions_to_Mars/templates/index.html) that takes the mars data dictionary and display all of the data in the appropriate HTML elements. Screenshots of the final web app can be found below.

![Mission to Mars Web Page - Top.png](Missions_to_Mars/images/Mission%20to%20Mars%20Web%20Page%20-%20Top.png)
![Mission to Mars Web Page - Bottom.png](Missions_to_Mars/images/Mission%20to%20Mars%20Web%20Page%20-%20Bottom.png)

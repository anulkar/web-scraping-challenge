# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup, UnicodeDammit
from urllib.parse import urlparse
import requests
import pymongo
import pandas as pd

# To use splinter create a new Chrome headless Browser instance
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser1 = Browser('chrome', **executable_path, headless=False)

# URL of Nasa Mars News Site that we want to scrape
nasa_mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Visit the Nasa Mars News Site
browser1.visit(nasa_mars_news_url)

# Scrape the NASA Mars News Site and retrieve the latest News Title and Paragraph Text

# Collect the latest News Title and Paragraph Text
# Initialize lists to save titles and teasers (i.e. paragraph texts)
news_titles = []
news_teasers = []

# Get the HTML content of the visited page
nasa_mars_news_html = browser1.html

# Create BeautifulSoup object; parse with lxml parser
nasa_news_soup = BeautifulSoup(nasa_mars_news_html, 'lxml')

news_listings = nasa_news_soup.find_all('div', class_='list_text')

print(f"STARTING to Scrape the site: {nasa_mars_news_url}")
print("---------------------------")
# Loop through news listings
for news_listing in news_listings:
    try:
        # Retrieve the news title and save to a list
        news_title = news_listing.find('div', class_='content_title').find('a').text
        news_titles.append(news_title)

        # Retrieve the news paragraph text/teaser and save to a list
        news_teaser = news_listing.find('div', class_='article_teaser_body').text
        news_teasers.append(news_teaser)
        
        print(f"News Title: {news_title}")
        print(f"News Teaser: {news_teaser}")
        print("---------------------------")
    except AttributeError as e:
        print(e)
print(f"DONE with Scraping {len(news_titles)} News Titles and {len(news_teasers)} News Teasers")
print("---------------------------")

# Find the image URL for the current Featured Mars Image on the JPL Mars Space Images page

# URL of JPL Mars Space Images Site that we want to scrape
jpl_mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# Visit the JPL Mars Space Images Site using splinter to create a new Chrome headless Browser instance
browser2 = Browser('chrome', **executable_path, headless=False)
browser2.visit(jpl_mars_images_url)

# Get the HTML content of the visited page
jpl_mars_images_html = browser2.html

# Create BeautifulSoup object; parse with lxml parser
jpl_images_soup = BeautifulSoup(jpl_mars_images_html, 'lxml')

# Find the image url for the current Featured Mars Image
try:
    featured_image_href = jpl_images_soup.find('div', class_='default floating_text_area ms-layer').find('footer').find('a')['data-fancybox-href']
except AttributeError as e:
    print(e)

# Parse the JPL website URL and save a complete url string for the feature image
parsed_uri = urlparse(jpl_mars_images_url)
featured_image_url = f'{parsed_uri.scheme}://{parsed_uri.netloc}{featured_image_href}'
print(f"Found the following Featured Image on the JPL Mars Space Images site: {featured_image_url}")

# Visit the Mars Weather twitter account and scrape the latest Mars weather tweet containing the weather report tweet text

# URL of Twitter page to be scraped
mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
browser3 = Browser('chrome', **executable_path, headless=False)
browser3.visit(mars_twitter_url)

# Get the HTML content of the visited page
mars_twitter_html = browser3.html

# Create BeautifulSoup object; parse with lxml parser
mars_twitter_soup = BeautifulSoup(mars_twitter_html, 'lxml')

# Retrieve the span tag for the specific class that holds all the tweet texts
mars_weather_tweets = mars_twitter_soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

# Loop through each tweet resultset
for mars_weather_tweet in mars_weather_tweets: 
    try:
        # Convert tweet text to lower case
        mars_weather = mars_weather_tweet.text
        lcase_mars_weather = mars_weather.lower()

        # All Mars Weather tweets begin with the text "insight sol", so we only look for those tweets
        if lcase_mars_weather.startswith('insight sol'):
            # Remove the "InSight" word from the tweet text
            mars_weather = mars_weather.replace("InSight ", "")
            # Print the weather tweet and break from loop
            print("Here is the latest weather report tweet from Mars Twitter")
            print("----------------------------------------------------------")
            print(mars_weather)
            break
        else:
            # Continue looping until we find the weather tweet
            continue
    except AttributeError as e:
        print(e)

# Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

# URL of Mars Facts webpage to be scraped
mars_facts_url = 'https://space-facts.com/mars/'

# Use the `read_html` function in Pandas to automatically scrape tabular data from the page
# What we get in return is a list of DataFrames for any tabular data that Pandas found
mars_facts_tables = pd.read_html(mars_facts_url)

# Slice off the first Mars Facts DataFrame that we want using normal indexing
mars_facts_df = mars_facts_tables[0]

# Rename the DataFrame columns
mars_facts_df.columns = ['Description', 'Value']

# Set the index to the Description column and print to verify
mars_facts_df.set_index('Description', inplace=True)
mars_facts_df

# Visit the [USGS Astrogeology site to obtain high resolution images for each of Mars' Hemispheres.

# URL of USGS Astrogeology site to be scraped
usgs_astrogeo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# Retrieve page with the requests module
browser4 = Browser('chrome', **executable_path, headless=False)
browser4.visit(usgs_astrogeo_url)

# Dictionary and List to hold the image URLs and Titles of Mars' Hemispheres
mars_hemisphere_image_dict = {}
mars_hemisphere_image_urls = []

# Iterate through each of the 4 Mars' Hemispheres pages
for x in range(4):
    try:
        # Click the link to go to the appropriate Hemisphere's "Enhanced" page 
        if x == 0:    
            browser4.click_link_by_partial_text('Cerberus')
        elif x == 1:
            browser4.click_link_by_partial_text('Schiaparelli')
        elif x == 2:
            browser4.click_link_by_partial_text('Syrtis')
        else:
            browser4.click_link_by_partial_text('Valles Marineris')

        # Get the HTML content of the visited page
        usgs_astrogeo_html = browser4.html

        # Create BeautifulSoup object; parse with lxml parser
        usgs_astrogeo_soup = BeautifulSoup(usgs_astrogeo_html, 'lxml')

        # Retrieve the full image URL and title of the hemisphere
        full_image_url = usgs_astrogeo_soup.find('div', class_='downloads').find('li').find('a')['href']
        mars_hemispheres_title = usgs_astrogeo_soup.find('h2', class_='title').text

        # Store the image URL and title into a dictionary and then append it to a list
        mars_hemisphere_image_dict = {"title": mars_hemispheres_title, "img_url": full_image_url}
        mars_hemisphere_image_urls.append(dict(mars_hemisphere_image_dict))

        # Go back to the main page so we can click on the next Hemisphere page link
        browser4.back()
    except Exception as e:
        print(e)

# Print the list of dictionaries
print(mars_hemisphere_image_urls)
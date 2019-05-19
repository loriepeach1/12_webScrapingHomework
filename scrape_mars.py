# Bootcamp Homework
# Week 12-Web-Scraping-and-Document-Databases
# loriepeach1@yahoo.com
#!/usr/bin/env python
# coding: utf-8

#import dependencies
from splinter import Browser
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt


def init_browser():
    # @NOTE: ensure chromedriver.exe is in the same directory as this file.  OR, change path
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


#this section applies to all fucntions created in this file

def scrape_all():

    # Initiate driver - confirm chromedrive.exe is in the same directory as this file NOTE:   different for MAC users
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_p = mars_news()

    # Each scraping function will store the results in a dictionary.   Define the dictionaries.
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(),
        "hemispheres": hemispheres(),
        "weather": twitter_weather(),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# ### Part 1.1 - NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.  https://mars.nasa.gov/news/


def mars_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get the first item, then wait 1 second
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1.0)

    html = browser.html
    newsSoup = bs(html, "html.parser")

    try:
        slide_elem = newsSoup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    # Stop webdriver and return data
    browser.quit()
    return news_title, news_p



# ### Part 1.2 - JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image here.  https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image 
# and assign the url string to a variable called featured_image_url.
# 
# * Make sure to find the image url to the full size .jpg image.
# 
# * Make sure to save a complete url string for this image.

def featured_image():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find & click the more info button
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()

    # create soup object to parse the XML
    html = browser.html
    imageSoup = bs(html, "html.parser")

    # Find the relative image url
    img = imageSoup.select_one("figure.lede a img")

    try:
        img_url_rel = img.get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    # Stop webdriver and return data
    browser.quit()
    return img_url



# ### Part 1.3 - Mars Weather
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called mars_weather.
# https://twitter.com/marswxreport?lang=en


def twitter_weather():
    browser = init_browser()
    
    #navigate to the site which will be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    # Retrieve page with the requests module
    response = requests.get(url)
    
    # Create BeautifulSoup object of this URL with the featured image; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    
    #from the beautifulSoup, retrieve the link for the page containing the details of the image.  attribute = data-link.    
    #NOTE:  since the instructions were to retrieve only the first weather report, then no index numbers
    #because the first record is always returned

    #as per example in homework instruction, the leading 'Insight' should not be present.
    #Therefore, this was added:   .split(None, 1)[1]

    latestWeather = soup.find('div',{"class": "js-tweet-text-container"}).text.split(None, 1)[1]
    
    # Stop webdriver and return data
    browser.quit()
    return (latestWeather)
    


# ### Part 1.4 - Mars Facts
# 
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# https://space-facts.com/mars/
# 
# * Use Pandas to convert the data to a HTML table string.


def mars_facts():
    browser = init_browser()
    #NOTE:  don't forget, import pandas as pd 

    #define the url
    url = 'https://space-facts.com/mars/'
    
    #this will return all tables found.  (per eyeball check, on this page, there is only one table.)
    tables = pd.read_html(url)
    
    #convert the table to a dataframe.   NOTE:   the [0] indicates the first table.  If there were more than one, remember to set the index.
    marsFacts_df = tables[0]
    marsFacts_df.columns = ['FactName', 'FactValue']
    
    #now that we have the df, convert it back to an HTML table
    mars_HTML_table = marsFacts_df.to_html()
    
    # Stop webdriver and return data
    browser.quit()
    return mars_HTML_table
    

# ### Part 1.5 - Mars Hemispheres
# 
# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres. 
#  https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing 
# the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

def scrape_hemisphere(html_text):

    # Soupify the html text
    hemi_soup = bs(html_text, "html.parser")

    # Try to get href and text except if error.
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:

        # Image error returns None for better front-end handling
        title_elem = None
        sample_elem = None

    hemisphere = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemisphere

def hemispheres():
     
    browser = init_browser()
    # Long URL can be on 2 lines as follows:
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)

    # to obtain the herf, click the link
    hemisphere_image_urls = []
    for each in range(4):

        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[each].click()

        hemi_data = scrape_hemisphere(browser.html)

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)

        # navigate back
        browser.back()
 
    # Stop webdriver and return data
    browser.quit()
    return hemisphere_image_urls




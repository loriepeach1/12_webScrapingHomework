#!/usr/bin/env python
# coding: utf-8

# In[929]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd


# ## Step 1 - Scraping
# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
# 
# <P> Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

# ### Part 1.1 - NASA Mars News
# 
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.  https://mars.nasa.gov/news/

# In[930]:


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[931]:


# Define database and collection
db = client.marsArticles_db
collection = db.articles


# In[932]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[933]:


# Retrieve page with the requests module
response = requests.get(url)


# In[934]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')
#soup = BeautifulSoup(response.text, 'lxml')


# In[935]:


#find the container which hold each article title and description
#results are returned as an iterable list
results = soup.find_all('div', class_='slide')


# In[936]:


#view the results to confirm the data.  'eyeball check'
print(results)


# In[937]:


# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        news_title = result.find('div', class_="content_title").text.strip()
        #Identify the news text
        news_text = result.find('div', class_="rollover_description_inner").text.strip()


        # Print results only if news title and news text are available
        if (news_title and news_text):
            print('-------------')
            print(news_title)
            print(news_text)
            
         # Dictionary to be inserted as a MongoDB document
            post = {
                'news_title': news_title,
                'news_text': news_text
            }

            collection.insert_one(post)
            
    except AttributeError as e:
        print(e)
        
    
# ??   how do  I remove the extra hard returns?


# In[938]:


# Display items in MongoDB collection
listings = db.articles.find()

for listing in listings:
    print(listing)


# #### Part 1.1 is complete.   
# The page has been scraped and the results stored in the articles collection of a mongo database.   within the collection, the variable names are:    news_title and news_text

# ### Part 1.2 - JPL Mars Space Images - Featured Image
# 
# 
# * Visit the url for JPL Featured Space Image here.  https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
# 
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# 
# 
# * Make sure to find the image url to the full size .jpg image.
# 
# 
# * Make sure to save a complete url string for this image.

# In[939]:


#NOTE:   I did not use splinter.  Re:  it was not needed as all the links were provided in the HTML.

#ensure Chrome Driver is in the same directory as this notebook.   (Different for MAC user)
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#navigate to the site which will be scraped
urlBase = 'https://www.jpl.nasa.gov'
urlSearch = '/spaceimages/?search=&category=Mars'
url12 = urlBase + urlSearch
browser.visit(url12)


# In[940]:


print(url12)


# Lorie's notes for location of the images
# 
# The 'Full Image button has the following:
# <P>
# <a class="button fancybox" data-description="Like a drop of dew hanging on a leaf, Tethys appears to be stuck to the A and F rings from this perspective of NASA's Cassini spacecraft." data-fancybox-group="images" data-fancybox-href="/spaceimages/images/mediumsize/PIA18284_ip.jpg" data-link="/spaceimages/details.php?id=PIA18284" data-title="Stuck on the Rings" id="full_image">
#     
# *data-fancybox-href is to a medium sized image - THIS ONE IS INCORRECT.  Need the full resolution, not the medium size.
#     <BR>**https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18284_ip.jpg
# 
# *data-link is to a page with the image and details.  From this page there is a link to DOWNLOAD the full resolution TFF and  vIEW the JPG
#     <BR>**https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA18284
#     
# Full TIFF - not needed for this project
#  https://photojournal.jpl.nasa.gov/tiff/PIA18284.tif
# 
# FULL JPG - this is needed.   Will be saved as a variable.
# https://photojournal.jpl.nasa.gov/jpeg/PIA18284.jpg

# In[941]:


# Retrieve page with the requests module
response12 = requests.get(url12)


# In[942]:


# Create BeautifulSoup object of this URL with the featured image; parse with 'html.parser'
soup12 = BeautifulSoup(response12.text, 'html.parser')


# In[943]:


#view to ensure the correct data ie, page
print(soup12.prettify())


# In[944]:


#from the beautifulSoup, retrieve the link for the page containing the details of the image.  attribute = data-link.    
#attribute is NOT data-fancybox-href.   This is a link to the MEDIUM sized image.  We need the full size image. 

imagePageDesc = soup12.find('a',{"class": "button fancybox"})['data-link']
print(imagePageDesc)


# In[945]:


#Create the URL to the description Page
url12a = urlBase + imagePageDesc
print(url12a)


# In[946]:


#the description page contains links to TWO images:   TFF and JPG.   
# Retrieve page with the requests module
response12a = requests.get(url12a)


# In[947]:


# Create BeautifulSoup object of this URL with the featured image; parse with 'html.parser'
soup12a = BeautifulSoup(response12a.text, 'html.parser')


# In[948]:


#view to ensure the correct data ie, page
print(soup12a.prettify())


# In[949]:


#from the beautifulSoup, find the links to the images
images = soup12a.find_all('div',{"class": "download_tiff"})
print(images)


# In[950]:


#data containign the JPG details
imageDataJ = soup12a.find_all('div',{"class": "download_tiff"})[1]
print(imageDataJ)


# In[951]:


#URL for the JPG Image
imageJ = imageDataJ.find('a')['href']
print(imageJ)


# In[952]:


#Create theURLs for both images
imageBase = "https:"
imageLinkJ = imageBase + imageJ

print("The URL for the jpg image is: " + imageLinkJ)


# #### Part 1.2 is complete.  

# ### Part 1.3 - Mars Weather
# 
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
# https://twitter.com/marswxreport?lang=en

# In[953]:


#ensure Chrome Driver is in the same directory as this notebook.   (Different for MAC user)
#DO NOT NEED TO DO since this was completed in this notebook in part 1.2
#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)

#navigate to the site which will be scraped
url13 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url13)


# In[954]:


# Retrieve page with the requests module
response13 = requests.get(url13)


# In[955]:


# Create BeautifulSoup object of this URL with the featured image; parse with 'html.parser'
soup13 = BeautifulSoup(response13.text, 'html.parser')


# In[956]:


#view to ensure the correct data ie, page
print(soup13.prettify())


# In[957]:


#from the beautifulSoup, retrieve the link for the page containing the details of the image.  attribute = data-link.    
#NOTE:  since the instructions were to retrieve only the first weather report, then no index numbers
#because the first record is always returned

#as per example in homework instruction, the leading 'Insight' should not be present.
#Therefore, this was added:   .split(None, 1)[1]

latestWeather = soup13.find('div',{"class": "js-tweet-text-container"}).text.split(None, 1)[1]
print(latestWeather)


# #### Part 1.3 is complete.  

# ### Part 1.4 - Mars Facts
# 
# 
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# https://space-facts.com/mars/
# 
# 
# * Use Pandas to convert the data to a HTML table string.

# In[958]:


#ASSUMPTION:    the entire page is called Mars Facts.   After viewing the HTML code, there is only one <table> element.   
# Therefore, I think this is the table referenced in the instructions.


# In[959]:


#if not already completed:
#import pandas as pd 

#define the url
url14 = 'https://space-facts.com/mars/'


# In[960]:


#this will return all tables found.  on this page, there is only one table.

tables = pd.read_html(url14)
tables


# In[961]:


type(tables)


# In[962]:


#convert the table to a dataframe.   NOTE:   the [0] indicates the first table.  If there were more than one, remember to set the index.
marsFacts_df = tables[0]
marsFacts_df.columns = ['FactName', 'FactValue']
marsFacts_df.head(20)


# In[963]:


#now that we have the df, convert it back to an HTML table

mars_HTML_table = marsFacts_df.to_html()
mars_HTML_table


# #### Part 1.4 is complete.  

# ### Part 1.5 - Mars Hemispheres
# 
# 
# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.  https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
# 
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[964]:


#if not already completed, do this:  (completed in step 1.2)
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#navigate to the site which will be scraped
url15base = 'https://astrogeology.usgs.gov'
url15_orig = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
url15 = url15base + url15_orig
browser.visit(url15)
print(url15)


# In[965]:


# results are returned as an iterable list
#results = soup15a.find_all('div', class_="item")


# In[966]:


# HTML object
html = browser.html
# Parse HTML with Beautiful Soup
soup15 = BeautifulSoup(html, 'html.parser')

# Retrieve all elements that contain hemisphere information
allList = soup15.find_all('div', class_="item")
#print(allList) #eyeball check


# In[967]:


#declare variables
title = []
page_url_list15 = []

# Iterate through each div item
for each in allList:
    
    #  retrieve the hemishpere title
    # to remove the last word use reverse split
    title15 = each.h3.text.rsplit(' ', 1)[0]
    title.append(title15)
    
    #  retrieve the URL for the page containing the link to the image
    linkExt = each.a['href']
    page_url_15 = url15base + linkExt
    page_url_list15.append(page_url_15)

    print('-----------')
    print(title15)
    print(page_url_15)


# In[968]:


#eyeball check
print(page_url_list15)


# In[969]:


#eyeball check
print(title)


# In[970]:


##############################################################
# now obtain the links to the high resolution jpg image
##############################################################


# In[971]:


#go to each page which will be scraped

#define an empty list for the image URLs
img_url = []

try: 
    for each in page_url_list15:

        #create results for that page
        browser.visit(each)

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup15b = BeautifulSoup(html, 'html.parser')
    
        # Retrieve all elements that contain hemisphere information
        allDownload = soup15b.find_all('div', class_="downloads")
        #print(allDownload)
    
        for each in allDownload:
            # retrieve the image URL
            imageURL15 = each.a['href']
    
            print('-----------')
            print(imageURL15)
                
            img_url.append(imageURL15)
 
except:
    print("The page structure is not as expected.  Please check the webpages have not changed HTML structure.  Error code: 1.5")


# In[972]:


print(img_url)


# In[973]:


##############################################################
# now that I have two lists, create a dictionary
# list of hemisphere titles =  title
# list of image URLS = img_url
##############################################################
#  ??  stuck - neither of these are correct per the example in the homework


# In[974]:


hemisphere_image_urls = dict(zip(title, img_url))


# In[975]:


print (hemisphere_image_urls)


# In[976]:


new_dict = {"title": [title], "img_url" : [img_url]}


# In[977]:


print(new_dict)


# #### Part 1.5 is incomplete.
# Need help on the last question for the dictionary

# ## Step 2 - MongoDB and Flask Application

# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# * **Part 2.1** 
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# * **Part 2.2**
# Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
# 
# * **Part 2.3**
# Store the return value in Mongo as a Python dictionary.
# 
# * **Part 2.4**
# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# * **Part 2.5**
# Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

# In[ ]:





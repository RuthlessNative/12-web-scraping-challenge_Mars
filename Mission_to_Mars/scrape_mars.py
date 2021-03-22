# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
## Dependencies
import time
#import shutil
import requests
import pandas as pd
from splinter import Browser
#from IPython.display import Image
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
## Module used to connect Python with MongoDb
import pymongo

# %% [markdown]
# # Step 1 - Scraping
# %% [markdown]
# ## NASA Mars News<br/>
# 1. Scrape the NASA Mars News Site (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

def scrape():

    # %%
    ## Setup splinter to open test browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## Give the browser time to open properly ("Run all cells" only)
    time.sleep(5)


    # %%
    ## URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    
    ## Opens test Chrome browser
    browser.visit(url)
    
    ## Allow page to fully load ("Run all cells" only)
    time.sleep(15)


    # %%
    ### Scrape page into Soup:

    ## Create HTML object
    html = browser.html

    ## Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')


    # %%
    ### Examine the results, then determine element that contains sought info. The original webpage may also be inspected on a browser
    #print(soup.prettify())


    # %%
    ### "content_title" & "article_teaser_body" are both found under class "list_text"

    ## soup.find_all results are returned as an iterable list
    ls_texts = soup.find_all("div", class_="list_text")
    #ls_texts


    # %%
    ## Get the first item in ls_texts
    ls_texts[0]


    # %%
    ### This For Loop returns title and paragraph text for each item in ls_texts (not needed to complete assignment)

    ## Loop through returned results
    for text in ls_texts:
        ## Error handling
        try:
            ## Identify and return title text
            title_text = text.find('div', class_="content_title").text
            ## Identify and return paragraph text
            p_text = text.find('div', class_='article_teaser_body').text

            ## Print results only if title_text and p_text are available
            if(title_text and p_text):
                print('-------------')
                print(f"{title_text}: ")
                print(p_text)
                
        except AttributeError as e:
            print(e)


    # %%
    ### These lines grab the title and paragraph texts of the first headline per assignment instructions

    ## Identify and return title text
    news_title = ls_texts[0].find('div', class_="content_title").text
    ## Identify and return paragraph text
    news_p = ls_texts[0].find('div', class_='article_teaser_body').text

    print(f"{news_title}: {news_p}")


    # %%
    ## Close the test browser
    browser.quit()
    ## Give the browser time to close properly ("Run all cells" only)
    time.sleep(5)

    # %% [markdown]
    # ## JPL Mars Space Images - Featured Image
    # 
    # 
    # 1. Visit the url for JPL Featured Space Image (https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html).
    # 
    # 2. Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # 
    # 3. Make sure to find the image url to the full size .jpg image.
    # 
    # 4. Make sure to save a complete url string for this image.

    # %%
    ## Setup splinter to open test browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## Give the browser time to open properly ("Run all cells" only)
    time.sleep(5)


    # %%
    ## URL of page to be scraped
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    ## Opens test Chrome browser
    browser.visit(url)

    ## Allow page to fully load ("Run all cells" only)
    time.sleep(15)


    # %%
    ### Design an XPATH selector to grab the featured image
    
    ## Right click HTML line holding button:
    ## (<button class="btn btn-outline-light"> FULL IMAGE</button>) -> 'Copy' -> 'Copy Full XPath'
    ## then paste below
    xpath = "/html/body/div[1]/div/a/button"


    # %%
    ## Use splinter to Click the 'FULL IMAGE' button to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()


    # %%
    ## Scrape the browser into soup and use soup to find the full resolution image of mars
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    ## Examine the results, then determine element that contains sought info. The original webpage may also be inspected on a browser
    #print(soup.prettify())


    # %%
    #### Save the image url to a variable called `img_url`
    ## "fancybox-image" holds the Featured Image, "src" holds the url tail end
    img_url = soup.find("img", class_="fancybox-image")["src"]

    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + img_url
    featured_image_url


    # %%
    ### Just for fun, not needed for assignment

    import shutil
    from IPython.display import Image
    
    # Use the requests library to download and save the image from the `img_url` above
    response = requests.get(featured_image_url, stream=True)
    with open('featured_img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


    # %%
    ### Just for fun, not needed for assignment

    # Display the image with IPython.display
    from IPython.display import Image
    Image(url='featured_img.png')


    # %%
    ## Close the test browser
    browser.quit()
    ## Give the browser time to close properly ("Run all cells" only)
    time.sleep(5)

    # %% [markdown]
    # ## Mars Facts
    # 
    # 
    # 1. Visit the Mars Facts webpage (https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # 2. Use Pandas to convert the data to a HTML table string.

    # %%
    ## Define the url
    url = "https://space-facts.com/mars/"


    # %%
    ## Use the `read_html` function in Pandas to automatically scrape any tabular data from a page
    tables = pd.read_html(url)
    ## Show list of tables
    tables


    # %%
    ## The table in tables[0] holds Mars data
    ## Pandas also had a `to_html` method that can be used to generate HTML tables from DataFrames
    tables[0].to_html("Mars_Facts.html") # this saves the filename in the parenthesis

    ## Save table in a variable for use in the Flask
    mars_facts = tables[0].to_html()

    ## or just use the code below to show the results:
    #tables[0].to_html()

    # %% [markdown]
    # ## Mars Hemispheres
    # 
    # 1. Visit the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # 2. You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # 3. Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # 
    # 4. Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # %%
    ## Setup splinter to open test browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## Give the browser time to open properly ("Run all cells" only)
    time.sleep(5)


    # %%
    ## URL of page to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    ## Opens test Chrome browser
    browser.visit(url)

    ## Allow page to fully load ("Run all cells" only)
    time.sleep(15)


    # %%
    ### Scrape page into Soup:

    ## Create HTML object
    html = browser.html

    ## Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')


    # %%
    ### Examine the results, then determine element that contains sought info. The original webpage may also be inspected on a browser
    #print(soup.prettify())


    # %%
    ## "content_title" & "article_teaser_body" are both found under class "list_text"

    ## soup.find_all results are returned as an iterable list
    ls_hemi_results = soup.find_all("div", class_="item")
    len(ls_hemi_results)


    # %%
    ### This For Loop finds the link of each Hemisphere in ls_hemi_results, goes to that link and parses it, then finds the "Wide-Image" link. Hemisphere title and Wide-Image links are stored in a dictionary.BufferError

    url = 'https://astrogeology.usgs.gov'

    ## Create an empty list of dictionaries
    hemisphere_image_urls = []

    ## Loop through returned results
    for item in ls_hemi_results:
        ## Error handling
        try:
            ## Identify and return Hemisphere name text
            hemi = item.find('div', class_="description").h3.text

            ## Identify and return Hemisphere link
            link_1 = url + item.a["href"]

            ## Go to link_1 that contains the full image link
            browser.visit(link_1)

            ## Create HTML object of the Hemiphere page
            link_2 = browser.html
            ## Create BeautifulSoup object; parse with 'html.parser'
            soup = bs(link_2, "html.parser")

            ## Identify and return Hemisphere "Wide-Image" file link
            link_3 = soup.find("img", class_="wide-image")["src"]

            ## Print results only if hemi, link_1 and link_2 are available
            if(hemi and link_1 and link_3):
                print('-------------')
                print(hemi)
                print(link_1)
                #print(link_2)
                print(link_3)

            ## Append the Hemisphere name text and "Wide-Image" file link to the dictionary list
            hemisphere_image_urls.append({"title": hemi, "img_url": url + link_3})

        except AttributeError as e:
            print(e)


    # %%
    hemisphere_image_urls


    # %%
    ## Close the test browser
    browser.quit()
    ## Give the browser time to close properly ("Run all cells" only)
    time.sleep(5)

    # %% [markdown]
    # # Step 2 - MongoDB and Flask Application
    # 
    # ## Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
    # 
    # 1. Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

    # %%
    ## NASA Mars News
    scrape_dict = {"News Title": news_title, 
                "News Paragraph": news_p,
                "Featured Image": featured_image_url,
                "Mars Facts": mars_facts,
                "Mars Hemishphere URLs": hemisphere_image_urls}
    scrape_dict

    return scrape_dict

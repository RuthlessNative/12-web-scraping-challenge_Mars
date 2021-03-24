# 12-web-scraping-challenge_Mars

1. Test and complete scraping within Jupyter notebook
    a. featured_image.png was created for fun and testing, needs to be commented out before converting this to a Python script (.py)
    
2. The last cell in the Jupyter notebook produces a list of dictionaries. These will be called on within our HTML (ex, mars["Mars Hemishphere URLs"][3]["img_url"])

3. The Jupyter notebook is then converted into a Python script (scrape_mars.py) and it's entire code is indented within _def scrape():_

4. app.py is created which renders the webpage from the templates -> index.html file. The scraping script, scrape_mars, is imported and called from within app.py

5. Click on the "Scrape New Data" button to do just that!

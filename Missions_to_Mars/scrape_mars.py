import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    # Create dictionary to store results
    results = {}

    # Create path to local chrome driver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Call url to open in local chrome driver
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Create Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Allow for time to load
    time.sleep(3)

    # Find news title and paragraph
    news_title = soup.find("div", class_="content_title").text.strip()
    news_p = soup.find("div", class_="article_teaser_body").text.strip()

    # Store results in dictionary 
    results['news_title'] = news_title
    results['news_paragraph'] = news_p


    # Call new url to open in local chrome driver
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url) 

    # Allow for time to load
    time.sleep(3)

    # Click into full image button
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    # Click into more info button
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()
    # Create Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Find link of image
    featured_image_article = soup.select_one("figure.lede a img").get("src")

    # Create full URL
    full_image_url = "https://jpl.nasa.gov"+featured_image_article
    # Append to dictionary
    results['featured_image'] = full_image_url


    # Call new url to open in local chrome driver
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url) 

    # Allow for time to load
    time.sleep(3)

    # Create Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Find location of weather tweet
    mars_weather = soup.find("div", class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o").text
    # Remove '/n' from sentence
    mars_weather.replace('\n', '')

    # Append to results dictionary
    results['mars_weather'] = mars_weather


    # Call new url to open in local chrome driver
    url = "https://space-facts.com/mars/"
    browser.visit(url) 

    # Allow for time to load
    time.sleep(3)

    # Create Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Read table from url and turn into DataFrame
    tables = pd.read_html(url)
    tables[0]
    df = tables[0]
    # Change column headers to Stat and Info; set Stat as index
    df.columns = ['Stat', 'Info']
    df.set_index('Stat', inplace=True)
    # Turn into an html table
    html_table = df.to_html()
    # Replace any '/n'
    html_table = html_table.replace('\n', '')

    # Append to results dictionary
    results['mars_facts_table'] = html_table

    # Call new url to open in local chrome driver
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url) 

    # Allow for time to load
    time.sleep(3)

    # Create Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Create hemisphere image dictionary
    hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
]

    # Append to results dictionary
    results['mars_hemispheres'] = hemisphere_image_urls

    # Quit browser
    browser.quit()


    return (results)
    
    

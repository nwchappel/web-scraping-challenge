import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def scrape():

    results = {}

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(3)

    news_title = soup.find("div", class_="content_title").text.strip()
    news_p = soup.find("div", class_="article_teaser_body").text.strip()

    results['news_title'] = news_title
    results['news_paragraph'] = news_p


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url) 

    time.sleep(3)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featured_image_article = soup.select_one("figure.lede a img").get("src")

    full_image_url = "https://jpl.nasa.gov"+featured_image_article
    results['featured_image'] = full_image_url


    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url) 

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.find("div", class_="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o").text
    mars_weather.replace('\n', '')

    results['mars_weather'] = mars_weather

    url = "https://space-facts.com/mars/"
    browser.visit(url) 

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    tables = pd.read_html(url)
    tables[0]
    df = tables[0]
    df.columns = ['Stat', 'Info']
    df.set_index('Stat', inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    results['mars_facts_table'] = html_table

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url) 

    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
]

    results['mars_hemispheres'] = hemisphere_image_urls

    browser.quit()


    return (results)
    
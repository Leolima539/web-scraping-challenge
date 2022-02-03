from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return  Browser('chrome', **executable_path, headless=False)
def scrape():

    # MARS News
    browser= init_browser
    url = "https://redplanetscience.com/"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Scrapping titles
    titles = soup.find('div', class_='content_title')
    for title in titles:
        news_title = title.text.strip()
        print(news_title)

    # Scrapping Paragraphs
    paragraphs = soup.find('div', class_='article_teaser_body')
    for paragraph in paragraphs:
        news_para = paragraph.text.strip()
        print(news_para)

    # Image

    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    img = soup.find("a", class_="showimg fancybox-thumbs")["href"]
    featured_image_url = image_url + img


    # Table

    table_url = 'https://galaxyfacts-mars.com'
    browser.visit(table_url)
    # Scrape page into Soup
    html = browser.html
    table = pd.read_html(html)
    table_df = table[1]
    table_df.columns =['Description', 'Value']


    # Hemispheres

    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    # Scrape all items that contain mars hemispheres information
    hemispheres = soup.find_all("div", class_="item")
    # Empty list to hold data
    h_info = []
    # Loop through the list of all hemispheres information
    for hemisphere in hemispheres:
        hemispheres_img = hemisphere.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = bs(image_html, "html.parser")
        title = hemisphere.find("h3").text
        img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
        h_info.append({"title" : title, "img_url" : img_url})

        

    mars_data = {
        "news": {
            "news_title": news_title,
            "news_paragraph": news_para,
            },
        "image": featured_image_url,
        "table": table_df,
        "hemispheres": h_info,
    }

    browser.quit()

    return mars_data
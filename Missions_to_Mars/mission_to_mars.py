
# Importing Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser(): 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)  

def scrape():
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    titles = soup.find('div', class_='content_title')
    for title in titles:
        news_title = title.text.strip()
        print(news_title)


    paragraphs = soup.find('div', class_='article_teaser_body')
    for paragraph in paragraphs:
        news_para = paragraph.text.strip()
        print(news_para)


    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find image url to the full size
    img = soup.find("a", class_="showimg fancybox-thumbs")["href"]
    featured_image_url = image_url + img
    featured_image_url


    table_url = 'https://galaxyfacts-mars.com'
    browser.visit(table_url)
    html = browser.html
    table = pd.read_html(html)

    table_df = table[1]
    table_df.columns =['Description', 'Value']
    table_df


    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find_all("div", class_="item")
    h_info = []

    # Loop through the list of all hemispheres information
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        hemispheres_img = hemisphere.find("a", class_="itemLink product-item")["href"]
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_url + hemispheres_img)
        
        # HTML Object
        image_html = browser.html
        web_info = bs(image_html, "html.parser")
        
        # Create full image url
        img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
        h_info.append({"title" : title, "img_url" : img_url})
        
    # Or Display titles and images ulr this way
        print(title)
        print(img_url)
    
    browser.quit()

    mars_info = {
            "title": news_title,
            "paragraph": news_para,
            "image": featured_image_url,
            "table": table_df,
            "hemispheres": h_info,
        }



    return mars_info
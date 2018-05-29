import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars['news_title'] = soup.find('div',class_="content_title").get_text()
    mars['news_p'] = soup.find('div',class_="article_teaser_body").get_text()
    


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('jpg')
    html= browser.html
    soup2 = BeautifulSoup(html,'lxml')
    mars["img_src"] = soup2.find('img')['src']


    
    # 3 Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    weather_soup = BeautifulSoup(html,'html.parser')
    find1 = weather_soup.find('div',attrs = {"class":'tweet',
                                         "data-name":'Mars Weather'})
    mars["Mars_Weather"] = find1.find('p',attrs={"class":"tweet-text"}).text


    # 4 Mars Facts
    url = 'http://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df.columns = ["description","values"]
    df.set_index('description',inplace=True)
    table = df.to_html()
    table = table.replace('\n', '')
    mars['facts'] = table


    ## 5 Mars Hemisperes

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    items = soup.find("div",{"id":"product-section"}).find_all("div",{"class":"item"})

    hemisphere_image_urls = []

    for item in items:
        img_main_url = "https://astrogeology.usgs.gov"+item.find("a")["href"]
        img_title = item.find("div",{"class":"description"}).find("a").find("h3").text
        browser.visit(img_main_url)
        time.sleep(1)
        img_soup = BeautifulSoup(browser.html,"html.parser")
        download_item = img_soup.find("div",{"class":"downloads"})
        hemisphere_item = {
            
            "img_url": download_item.find("li").find("a")["href"]
        }
        hemisphere_image_urls.append(hemisphere_item)
    
    mars["hemispheres"] = hemisphere_image_urls






    browser.quit()

    return mars

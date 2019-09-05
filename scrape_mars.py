import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

#Function list:
    #init_browser()
    #scrape_news()
    #scrape_image()
    #scrape_tweets()
    #scrape_facts()
    #scrape_hemispheres()


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_news():
    browser = init_browser()
    url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    headlines= soup.find_all("li", class_="slide")
    news_title=headlines[0].find("h3").text
    news_p=headlines[0].a.text
    results = {"title":news_title,"p":news_p}
   
    # Close the browser after scraping
    browser.quit()
    return results

def scrape_image():
    browser = init_browser()
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all("article", class_="carousel_item")
    image_url=results[0].find("a")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov"+ image_url
    
    # Close the browser after scraping
    browser.quit()
    return featured_image_url



def scrape_tweets():
    browser = init_browser()
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = results[0].text
    
    # Close the browser after scraping
    browser.quit()
    return mars_weather

def scrape_facts():
    browser = init_browser()
    url="https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results=soup.find_all("table", class_="tablepress tablepress-id-p-mars")
    result = str(results[0])
    with open("facts_table.html", "w") as file:
        file.write(result)
    #Close the browser after scraping
    browser.quit()
    return result


def scrape_hemispheres():
    browser = init_browser()
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results=soup.find_all("h3")
    #results:
    #[<h3>Cerberus Hemisphere Enhanced</h3>,
     #<h3>Schiaparelli Hemisphere Enhanced</h3>,
     #<h3>Syrtis Major Hemisphere Enhanced</h3>,
     #<h3>Valles Marineris Hemisphere Enhanced</h3>]
    
    hemisphere_image_urls=[]
    
    #Get the link of the image in each name
    for result in results:
        title=result.text
        
        #name =text_str.split(' Hemisphere ')[0].lower().replace(" ","_")
        #enhanced =text_str.split(' Hemisphere ')[1].lower()
        #link_name = name+"_"+ enhanced
        
        #Click the according links to get the image's link
        url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(1)
        
        browser.click_link_by_partial_text(title)
        
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        #Get the relative link in the webpage
        link = soup.find("img", class_="wide-image")
        #Create a complete link of the image
        img_url = "https://astrogeology.usgs.gov" + link["src"]
        
        info_dict = {"title":title,"img_url":img_url}
        hemisphere_image_urls.append(info_dict)
        
    #Close the browser after scraping
    browser.quit()
    return hemisphere_image_urls
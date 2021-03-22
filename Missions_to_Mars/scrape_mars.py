from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #--------------------NASA NEWS SCRAPE-----------------------------
    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = bs(html, 'html.parser')

    content_title = news_soup.find_all(class_='content_title')
    body_article = news_soup.find_all(class_='article_teaser_body')

    news_title=[]
    news_paragraph = []

    for title in content_title:
        try:
            news_title.append(title.a.text.strip())
        except:
            pass
        
    for body in body_article:
        try:
            news_paragraph.append(body.text.strip())
        except:
            pass
        
    recent_news = news_title[0]
    recent_paragraph = news_paragraph[0]
    news_dict = {}
    news_dict['news title'] = recent_news
    news_dict['news paragraph'] = recent_paragraph

    #-----------------------JPL SCRAPE------------------------
    # JPL Website
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    # Open chrome and visit url
    browser.visit(jpl_url)

    html = browser.html

    jpl_soup = bs(html, 'html.parser')

    main_image = jpl_soup.find_all('img', class_='headerimage')
    for image in main_image:
        featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image['src']}"
    jpl_dict = {}
    jpl_dict['img url'] = featured_image_url
    

    #---------------------------MARS FACTS SCRAPE------------------
    # Scraped table containing facts about the planet
    mars_url = 'https://space-facts.com/mars/'

    # Read url and returned a list of DataFrames
    mars_table = pd.read_html(mars_url)
    mars_table = mars_table[1]

    # Converted data to HTML table string
    html_mars_table = mars_table.to_html()
    mars_dict = {}
    mars_dict['mars table'] = html_mars_table

    #-------------------HEMISPHERES SCRAPE-------------------------
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    names = soup.find_all(class_='description')

    # Create a list of hemisphere names to be used to iterate over them to navigate on the next loop
    hemisphere_list = []
    for name in names:
        hemisphere_list.append(name.a.h3.text)

    # Navigate through all pages and get the full resolution hemisphere image
    browser.visit(hemispheres_url)
    hemisphere_image_urls=[]
    for i in range(len(hemisphere_list)):
            html = browser.html
            soup = bs(html, 'html.parser')
            browser.click_link_by_partial_text(hemisphere_list[i])
            html = browser.html
            soup = bs(html, 'html.parser')
            title = hemisphere_list[i]
            img_url = soup.find(class_='downloads')
                
            hemisphere_dict = {}
            hemisphere_dict['title'] = title
            hemisphere_dict['img_url'] = img_url.a['href']
            hemisphere_image_urls.append(hemisphere_dict)
            browser.back()

    #Adding everything into dictionaries/lists
    nasa_data = []
    nasa_data.append(news_dict)
    nasa_data.append(jpl_dict)
    nasa_data.append(mars_dict)
    nasa_data.append(hemisphere_dict)

    #Close browser with splinter
    browser.quit()

    return nasa_data
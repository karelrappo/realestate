import time
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pandas as pd
from datetime import datetime
import os
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Create the options - i.e. enable javascript and disable automation flag
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-fullscreen")


class WebPage:
    """Creates a WebDriver instance that can be used across functions. """
    Instance = None

    def __init__(self):
        self.driver = webdriver.Chrome(options=options)

    def parser(self, url):
        """ Opens the URL passed to the function, and returns parsed html"""
        self.driver.get(url)
        time.sleep(2)
        # Agrees with the cookies if it is present
        try:
            self.driver.find_element_by_id(
                "onetrust-accept-btn-handler").click()
        except:
            pass
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def quit(self):
        self.driver.quit()

def get_properties(url, count):
    """Loops through all pages of listings, and saves their urls into list."""
    all_links = []
    for i in tqdm(range(1, count+1)):
        page_url = url+str(i)
        soup = browser.parser(page_url)
        results = soup.find_all("tr", class_="object-type-apartment object-item")
        for property in results:
            links = property.find_all("a",{"class":"object-title-a text-truncate"})
                for link in links:
                    all_links.append(link['href'])
    return all_links


##################################### FROM NOTEBOOK ##########
def Properties_info(i):
    d = {}
    Parser(links[i])
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
    except:
        pass
    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_content = soup.find("div", {"class": "object-article-details"})
        price = page_content.find("div", {"class": "object-price"}).findChildren()[0]
        descr = soup.find("div", {"class": "object-article-body"}).find("p")
        aadress = soup.find('h1', {'class': 'title'}).get_text(strip=True)
        # loop through rows in info table
        for items in page_content.find('table', {"class": "table-lined object-data-meta"}).find_all('tr'):
            data = [item.get_text(strip=True) for item in items.find_all(['th', 'td'])]
            d[data[0]] = data[-1]
            d['url'] = links[i]
            d['hind'] = price.get_text(strip=True)
            d['aadress'] = aadress
            d['description'] = descr
            d['date'] = today
    all_info.append(d)

for i in tqdm(range(0,len(links))):
    Properties_info(i)
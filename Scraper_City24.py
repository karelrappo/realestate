# Import packages
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pandas as pd
from datetime import datetime
import os

# Create the options - i.e. enable javascript and disable automation flag
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript");
options.add_argument("--dns-prefetch-disable");
options.add_argument("--disable-gpu");
options.add_argument("--disable-blink-features=AutomationControlled");
options.add_argument("--start-fullscreen");

## Scraper
class WebPage:
    """Creates a WebDriver instance that can be used across functions. """
    Instance = None
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)

    def parser(self, url):
        """ Opens the URL passed to the function, and returns parsed html"""
        self.driver.get(url)
        time.sleep(2)
        #Agrees with the cookies if it is present
        try:
            self.driver.find_element_by_id(
                "_hj-wTnOw__SurveyInvitation__noThanksButton _hj-3OscV__styles__clearButton").click()
        except:
            pass
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup
    def quit(self):
        self.driver.quit()

## Function for extracting the info from properties
def get_info(url):
    """Opens up the property, and stores the info"""
    d = {}
    soup = browser.parser(url)
    try:
        address = soup.find("div", {"class": "obj-detail__address"}).get_text()
    except Exception:
        address = "N/A"
    try:
        linnaosa = soup.find("div", {"class": "obj-detail__area"}).get_text()
    except Exception:
        linnaosa = "N/A"
    # Find all tables on the pages
    tables = soup.find_all("table",{"class":"full-specs"})
    # Extract the body of the tables and append to the list
    table_contents = []
    for table in tables:
        table_contents.append(table.find_all("tbody"))
    # Loop through table contents and extract all rows
    for table_content in table_contents:
        for items in table_content[0].find_all("tr"):
        # Create a cleaned list with items and values
            data = [item.get_text(separator=',') for item in items.find_all(['th', 'td'])]
            d[data[0]] = data[-1]
            d['Aadress'] = address + ',' + linnaosa
            d['Kuupaev'] = today
    return(d)

def get_pages(url):
    """Checks how many pages are for a given search"""
    soup = browser.parser(url)
    count = int(soup.find_all("a",{"class":"page__number"})[-1].get_text())
    print(f"There are {count} pages for your search!")
    return count

def get_properties(url, count):
    """Loops through all pages of listings, and saves their urls into list."""
    all_links = []
    for i in tqdm(range(1, count+1)):
        page_url = url+str(i)
        soup = browser.parser(page_url)
        results = soup.find_all("article", {"class": "object-wrapper"})
        for property in results:
            link = property.find_all("a", class_="object__attributes")[0]['href']
            all_links.append("https://city24.ee" + link)
    return all_links

def user_inputs():
    """Get the inputs from the user for search"""
    SUPPORTED_BUILDINGS = ['houses','apartments']
    SUPPORTED_TYPES = ['sale', 'rent']
    SUPPORTED_COUNTIES = ['voru', 'harju', 'valga', 'tartu', 'polva', 'viljandi', 'parnu', 'saare', 'hiiu', 'rapla',
                          'jarva', 'jogeva', 'rapla', 'ida-viru', 'laane-viru', 'laane']

    COUNTY_DICT = {'voru': 20271, 'harju': 1, 'valga': 14, 'tartu': 20269,
                   'polva': 20266, 'viljandi': 20267, 'parnu': 20267,
                   'saare': 11, 'hiiu': 2, 'rapla': 20268, 'jarva': 20263, 'jogeva': 20262,
                   'rapla': 20268, 'ida-viru': 20261, 'laane-viru': 20265, 'laane': 20264}

    LISTING_TYPE = ""
    COUNTY = ""
    BUILDING_TYPE = ""
    while BUILDING_TYPE not in SUPPORTED_BUILDINGS:
        print(f"Available building types are: {SUPPORTED_BUILDINGS}. Default is 'apartments'.")
        BUILDING_TYPE = (input("Enter the building type: ") or 'apartments')
    while LISTING_TYPE not in SUPPORTED_TYPES:
        print(f"Available listing types are: {SUPPORTED_TYPES}. Default is 'sale'.")
        LISTING_TYPE = (input("Enter the listing type: ") or 'sale')
    while COUNTY not in SUPPORTED_COUNTIES:
        print(f"Available counties are: {SUPPORTED_COUNTIES}. Default is 'harju.")
        COUNTY = (input("Enter the listing type: ") or 'harju')
    county_code = COUNTY_DICT.get(COUNTY)
    url = f"https://www.city24.ee/real-estate-search/{BUILDING_TYPE}-for-{LISTING_TYPE}/{COUNTY}-maakond/id={county_code}-county/pg="
    return url, BUILDING_TYPE, LISTING_TYPE, COUNTY

def main():
    """Main function that runs everything"""
    dataset = []
    url, BUILDING_TYPE, LISTING_TYPE, COUNTY = user_inputs()
    count = get_pages(url)
    print(f"Started scraping links at {datetime.now().time()}")
    links = get_properties(url, count)
    print(f"Stopped scraping links at {datetime.now().time()}")

    savedir = f"./data/{today}/{BUILDING_TYPE}/{LISTING_TYPE}/{COUNTY}"
    os.makedirs(savedir, exist_ok=True)
    pd.DataFrame(links).to_csv(f"{savedir}/links.csv")

    print(f"Started scraping data at {datetime.now().time()}")
    for i in tqdm(range(0,len(links))):
        dataset.append(get_info(links[i]))
    df = pd.DataFrame(dataset)
    df['maakond'] = COUNTY

    df.to_csv(f"{savedir}/properties.csv")
    browser.quit()

if __name__ == "__main__":
    browser = WebPage()
    today = datetime.today().strftime('%Y-%m-%d')
    main()
import time
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pandas as pd
from datetime import datetime
import os
from webdriver_manager.chrome import ChromeDriverManager
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Create the options - i.e. enable javascript and disable automation flag
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-fullscreen")

class SearchArguments:
    def __init__(self, listing_type=None, county=None, building_type=None):
        self.listing_type = listing_type
        self.county = county
        self.building_type = building_type

    def county_mapper(self):
        county_dict = {'voru': 20271, 'harju': 1, 'valga': 14, 'tartu': 20269,
                       'polva': 20266, 'viljandi': 20267, 'parnu': 20267,
                       'saare': 11, 'hiiu': 2, 'jarva': 20263, 'jogeva': 20262,
                       'rapla': 20268, 'ida-viru': 20261, 'laane-viru': 20265, 'laane': 20264}
        return(county_dict.get(self.county))

    def url_generator(self):
        base_url = "https://www.city24.ee/real-estate-search"
        county_code = self.county_mapper()
        return (f"{base_url}/{self.building_type}-for-{self.listing_type}/{self.county}-maakond/id={county_code}-county/pg=")


# Scraper
class WebPage:
    """Creates a WebDriver instance that can be used across functions. """
    Instance = None

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def parser(self, url):
        """ Opens the URL passed to the function, and returns parsed html"""
        self.driver.get(url)
        time.sleep(2)
        # Agrees with the cookies if it is present
        try:
            self.driver.find_element_by_id(
                "_hj-wTnOw__SurveyInvitation__noThanksButton _hj-3OscV__styles__clearButton").click()
        except:
            pass
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def quit(self):
        self.driver.quit()


def get_pages(url):
    """Checks how many pages are for a given search"""
    soup = browser.parser(url)
    count = int(soup.find_all("a", {"class": "page__number"})[-1].get_text())
    print(f"There are {count} pages for your search!")
    return count


def get_properties(url, count):
    """Loops through all pages of listings, and saves data of properties into list."""
    dataset = []
    for i in tqdm(range(1, count+1)):
        page_url = url+str(i)
        soup = browser.parser(page_url)
        listings = soup.find_all("article", {"class": "object-wrapper"})
        for property in listings:
            d = {}
            rooms = ""
            floors = ""
            area_outside = ""
            area = ""
            link = ""
            address = ""
            hind = ""
            for attributes in property.find_all("a", class_="object__attributes"):
                link = "https://city24.ee" + attributes['href']
                address = attributes['title']
                for item in attributes.find_all('li'):
                    if item.find("span", {"class": "icon-door"}) is not None:
                        rooms = item.get_text().strip()
                    elif item.find("span", {"class": "icon-stairs"}) is not None:
                        floors = item.get_text().strip()
                    elif item.find("span", {"class": "icon-land"}) is not None:
                        area_outside = item.get_text().strip()
                    else:
                        area = item.get_text().strip()
            d['rooms'] = rooms
            d['floors'] = floors
            d['area_outside'] = area_outside.split(" ")[0]
            d['area'] = area.split(" ")[0]
            d['link'] = link
            d['address'] = address
            d['date'] = today
            try:
                d['hind'] = float(property.find("div", {"class": "object-price__main-price"})
                                    .get_text().replace(u'\xa0', u''))
            except:
                d['hind'] = 0
            dataset.append(d)
    return dataset


def user_inputs():
    """Get the inputs from the user for search"""
    supported_buildings = ['houses', 'apartments']
    supported_types = ['sale', 'rent']
    supported_counties = ['voru', 'harju', 'valga', 'tartu', 'polva', 'viljandi', 'parnu', 'saare', 'hiiu', 'rapla',
                          'jarva', 'jogeva', 'rapla', 'ida-viru', 'laane-viru', 'laane']

    while Search.building_type not in supported_buildings:
        print(f"Available building types are: {supported_buildings}. Default is 'apartments'.")
        Search.building_type = (input("Enter the building type: ") or 'apartments')
    while Search.listing_type not in supported_types:
        print(f"Available listing types are: {supported_types}. Default is 'sale'.")
        Search.listing_type = (input("Enter the listing type: ") or 'sale')
    while Search.county not in supported_counties:
        print(f"Available counties are: {supported_counties}. Default is 'harju.")
        Search.county = (input("Enter the listing type: ") or 'harju')


def main():
    """Main function that runs everything"""
    user_inputs()
    url = Search.url_generator()
    count = get_pages(url)
    savedir = f"./data/MinimalVersion/{today}/{Search.building_type}/{Search.listing_type}/{Search.county}"
    os.makedirs(savedir, exist_ok=True)
    print(f"Started scraping data at {datetime.now().time()}")
    dataset = get_properties(url, count)
    df = pd.DataFrame(dataset)
    df['maakond'] = Search.county
    df.to_csv(f"{savedir}/properties.csv")
    browser.quit()


if __name__ == "__main__":
    browser = WebPage()
    Search = SearchArguments()
    today = datetime.today().strftime('%Y-%m-%d')
    main()
    print("Scraping finished successfully!")

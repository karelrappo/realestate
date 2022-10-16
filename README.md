# Estonian Real Estate Scraper

Currently includes a scraper for real estate site https://www.city24.ee. Additional ones in development.

# What does it do, and how to use?
1. Run Scraper_City24.py and fill in the inputs
- Enter the county you want to scrape the data for (i.e. harju, tartu, valga etc.)
- Enter if you want to scrape the data for rentals or properties to be sold.
2. The Scraper loops through all of the pages for a given combination, and stores the urls for the given properties.
3. After having done so, it individually goes to each listing page, and obtains the most important information.
4. Keep in mind that the stored data is uncleaned, and requires additional efforts.

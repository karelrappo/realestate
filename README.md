# Real Estate Scraper for Estonian market.

Currently includes a scraper for real estate site https://www.city24.ee. kv.ee to be added later.

## What does it do, and how to use?
There are currently two versions of the scrapers -
- [one](https://github.com/karelrappo/realestate/blob/main/City24ScraperMin.py) that scrapes the high level data from search results
- [second](https://github.com/karelrappo/realestate/blob/main/City24Scraper.py) that gets detailed data from each page of the property

1. Run either script, and fill in the inputs prompted in the command line.
Inputs:
- County: harju, tartu, viljandi, etc. 
- Listing Type - sale, rental
- Building Type - apartments, houses 
2. The Scraper loops through all of the pages for a given combination, and stores the urls for the given properties.
3. After having done so, it individually goes to each listing page, and obtains the most important information.
4. Keep in mind that the scraper could run for ca 10h depending on the amount of listings, and specs of the computer.
5. Saved data is uncleaned, and requires additional efforts to make data suitable for analysis.

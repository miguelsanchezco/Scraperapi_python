import scrapy
from scraper_api import ScraperAPIClient
# pip install scraperapi-sdk

from Scraperapi.links_generator import links_generator

def ScraperAPI():
    API_KEY = 'd953019d893d570c75ab356c8a218a12'
    CONCURRENT_REQUESTS = 50
    CONCURRENT_REQUESTS_IP = 50
    RETRY_TIMES = 5
    return API_KEY, CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_IP, RETRY_TIMES

API_KEY, CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_IP, RETRY_TIMES = ScraperAPI()


"""
SCRAPER SETTINGS
You need to define the following values below:
- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup
To use this script you need to modify a couple settings in the settings.py file:
                
- CONCURRENT_REQUESTS  --> Set this equal to the number of concurrent threads available
                in your plan. For reference: Free Plan (5 threads), Hobby Plan (10 threads),
                Startup Plan (25 threads), Business Plan (50 threads), 
                Enterprise Plan (up to 5,000 threads).
- RETRY_TIMES  --> We recommend setting this to 5 retries. For most sites 
                95% of your requests will be successful on the first try,
                and 99% after 3 retries. 
- ROBOTSTXT_OBEY  --> Set this to FALSE as otherwise Scrapy won't run.
- DOWNLOAD_DELAY & RANDOMIZE_DOWNLOAD_DELAY --> Make sure these have been commented out as you
                don't need them when using Scraper API.
"""

client = ScraperAPIClient(API_KEY)

class QuotesSpider(scrapy.Spider):

    name = "sdk_metodo"

    custom_settings = {

            'FEED_URI' : 'sdk_metodo.csv', 
            'FEED_FORMAT' : 'csv',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'CONCURRENT_REQUESTS' : CONCURRENT_REQUESTS, #ScraperAPI  
            'RETRY_TIMES': RETRY_TIMES, # ScraperAPI Recommendation
            'ROBOTSTXT_OBEY' : False,
            'CONCURRENT_REQUESTS_PER_IP' : CONCURRENT_REQUESTS_IP #ScraperAPI  
        
    }

    def start_requests(self):

        urls = links_generator()
        #urls = ['http://quotes.toscrape.com/page/1/','http://quotes.toscrape.com/page/2/']
        for url in urls:
            yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse)

    def parse(self, response):

        price = 'null'
        title = 'null'   

        try:
            title = response.css('span#productTitle::text').get().replace('\n','')
            price = response.css('span#priceblock_ourprice::text').get().replace('\n','')
        except:
            pass

        yield { 

            'price':price,
            'title':title

        }

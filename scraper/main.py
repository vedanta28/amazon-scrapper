import requests
from bs4 import BeautifulSoup
from bottomTable import getdata
from reviews import AmazonReviewScraper
from productDetails import AmazonProductDetailsScraper
import time
from threading import Thread
import csv

url_list = []
def assign_fields(dictionary1, dictionary2):
    result = dictionary1.copy()
    for key in dictionary1:
        if key in dictionary2:
            result[key] = dictionary2[key]
    return result

filename = "data.csv"

master_dict = {
    "asin": "",
    "ranking": "",
    "date_first_available": "",
    "product_name": "",
    "price": "",
    "mrp": "",
    "is_dotd": "",
    "is_deal": "",
    "is_ld": "",
    "ratings_count": "",
    "rating": "",
    "status": "",
    "sold_by": "",
    "fba/mfn": "",
    "shipping_fee": ""
}

headers = {
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
}

#periodically run the scraper for all urls in the list
def process_urls():
    while True:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=master_dict.keys())
            writer.writeheader()
            print("Ohh would you look at the time! Time to work")
            for url in url_list:
                # Perform the desired operations on the URL
                print("Processing URL:", url)
                data = getdata(url)
                print(data)

                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text,  "lxml")
                data0 = AmazonProductDetailsScraper(soup)
                dict0 = assign_fields(master_dict, data0)
                
                dict1 = assign_fields(dict0, data)
                asin = dict1.get("asin", "")
                AmazonReviewScraper().scrape_reviews(asin, 100)
                print(dict1)
                writer.writerow(dict1)

        time.sleep(60)  # Wait for 1 minutes

# Start the background thread for URL processing
def start_processing_thread():
    thread = Thread(target=process_urls)
    thread.start()

if __name__ == '__main__':
    start_processing_thread()

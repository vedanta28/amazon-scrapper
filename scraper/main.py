import requests
from bs4 import BeautifulSoup
from bottomTable import getdata
from reviews import AmazonReviewScraper
from productDetails import AmazonProductDetailsScraper
import time
from datetime import datetime
from threading import Thread
import csv
import random

url_list = []

input_file = "input.txt"
filename = f"scrapped_data/{datetime.now().strftime('%Y-%m-%d-%m')}_product_details.csv"


def read_urls_from_file(filename):
    global url_list
    with open(filename, 'r') as file:
        urls = file.readlines()
    # Remove whitespace and newline characters from the URLs
    urls = [url.strip() for url in urls]
    url_list.extend(urls)  # Append the URLs to the global url_list variable

def assign_fields(dictionary1, dictionary2):
    result = dictionary1.copy()
    for key in dictionary1:
        if key in dictionary2:
            result[key] = dictionary2[key]
    return result

def get_details(dictionary1,dictionary2):
    result= dictionary1.copy()
    details_list=[]
    for key in dictionary2:
        if key not in dictionary1:
            details_list.append(key+" : "+dictionary2[key])
    result["details"]=" | ".join(details_list)
    return result

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
    "shipping_fee": "",
    "details": ""
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
    read_urls_from_file(input_file)
    # while True:
    start_time = time.time()
    cnt = 1
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=master_dict.keys())
        writer.writeheader()
        print("Ohh would you look at the time! Time to work")
        for url in url_list:
            # Perform the desired operations on the URL
            print(f"Processing URL {cnt}:", url)
            cnt += 1
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text,  "lxml")
            data = getdata(soup)
            data0 = AmazonProductDetailsScraper(soup).scrape_product_details()
            dict0 = assign_fields(master_dict, data0)
            dict1 = assign_fields(dict0, data)
            dict1 = get_details(dict1,data)
            # asin = dict1.get("asin", "")
            # AmazonReviewScraper().scrape_reviews(asin, 100)
            writer.writerow(dict1)
            time.sleep(random.randint(0, 1000) / 1000)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")

# Start the background thread for URL processing
def start_processing_thread():
    thread = Thread(target=process_urls)
    thread.start()

if __name__ == '__main__':
    start_processing_thread()

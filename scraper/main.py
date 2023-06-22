from bottomTable import getdata
from reviews import AmazonReviewScraper
import os
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
    "shipping_fee": "",
    "asin": "",
    "fba/mfn": "",
    "buy_box_price": "",
    "dotd_price": "",
    "sale_price": "",
    "deal_price": "",
    "date_first_available": "",
    "status": "",
    "is_dotd": "",
    "price": "",
    "rating": "",
    "ratings": "",
    "mrp": "",
    "product_name": "",
    "sold_by": "",
    "ranking": "",

}

#periodically run the scraper for all urls in the list
def process_urls():
    while True:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=master_dict.keys())
            writer.writeheader()
            print("ohh would you look at the time! time to work")
            for url in url_list:
                # Perform the desired operations on the URL
                print("Processing URL:", url)
                data = getdata(url)
                print(data)
                dict1 = assign_fields(master_dict, data)
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
    app.run()

from bottomTable import getdata
from reviews import AmazonReviewScraper
from pymongo import MongoClient
import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import csv


############################Future work: Database################################################

#load environment variables
with open('.env') as f:
    for line in f:
        key, value = line.strip().split('=')
        os.environ[key] = value

def dbConnector():
    conn_string=os.environ["CON_STR"]
    conn_string=conn_string.replace('<password>',os.environ["PASSWORD"])
    client = ""
    while client == "":
        try:
            client = MongoClient(conn_string)
        except:
            time.sleep(1)
            print("Error connecting to database.")

    # Access a specific database
    database = client[os.environ["DB_NAME"]]

    # Access a specific collection within the database
    collection = database["products"]
    return collection

##########################################################################################################

app = Flask(__name__)
CORS(app, origins="*") # Allow CORS requests from any origin
url_list = ["https://www.amazon.in/Harissons-Sirius-Laptop-Backpacks-Built/dp/B07MD1G8RZ/ref=cm_cr_arp_d_product_top?ie=UTF8"]
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

@app.route('/add-url', methods=['POST'])
def add_url():
    data = request.get_json()
    url = data.get('url')
    if url:
        url_list.append(url)
        return jsonify({"message": "URL added successfully"})
    else:
        return jsonify({"message": "No URL provided"}), 400

# Start the background thread for URL processing
def start_processing_thread():
    thread = Thread(target=process_urls)
    thread.start()

if __name__ == '__main__':
    start_processing_thread()
    app.run()

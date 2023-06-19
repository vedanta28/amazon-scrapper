from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
import re
import requests
import time
import json

def getdata(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=options)
    driver.get(url)
    time.sleep(1)
    #technical details
    Fields=driver.find_element(By.CSS_SELECTOR,"#productDetails_techSpec_section_1").find_elements(By.CSS_SELECTOR,".a-color-secondary.a-size-base.prodDetSectionEntry")
    Values=driver.find_element(By.CSS_SELECTOR,"#productDetails_techSpec_section_1").find_elements(By.CSS_SELECTOR,".a-size-base.prodDetAttrValue")
    Fields=[field.text for field in Fields]
    Values=[value.text for value in Values]
    #additional details
    Rows=driver.find_element(By.CSS_SELECTOR,"#productDetails_detailBullets_sections1").find_elements(By.TAG_NAME,"tr")
    for row in Rows:
        if(row.find_element(By.TAG_NAME,"th").text=="Customer Reviews"):
            Fields.append("Rating")
            Values.append(row.find_element(By.TAG_NAME,"td").find_element(By.CSS_SELECTOR,".a-size-base.a-color-base").text)
            Fields.append("Number of Reviews")
            Values.append(row.find_element(By.TAG_NAME,"td").find_element(By.CSS_SELECTOR,"#acrCustomerReviewText").text.split(" ")[0])
            continue
        if(row.find_element(By.TAG_NAME,"th").text=="Best Sellers Rank"):
            Fields.append(row.find_element(By.TAG_NAME,"th").text)
            #remove the bracket part and combine lines by "and"    
            text=row.find_element(By.TAG_NAME,"td").text
            text = re.sub(r'\([^()]*\)', '', text).replace('\n', ', ')
            Values.append(text)
            continue
        Fields.append(row.find_element(By.TAG_NAME,"th").text)
        Values.append(row.find_element(By.TAG_NAME,"td").text)

    n=len(Fields)

    res={}
    for i in range(n):
        res[Fields[i]]=Values[i]
    return res


# code to run and test
url="https://www.amazon.in/HP-Multi-Device-Bluetooth-Resistant-Auto-Detection/dp/B0BR3YKQQ1/ref=sr_1_2_sspa?keywords=keyboards&qid=1687188204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
url2="https://www.amazon.in/Kurkure-Namkeen-Masala-Munch-95g/dp/B004IF24XE/ref=sr_1_1?keywords=kurkure&qid=1687195614&sr=8-1"
JSON=json.dumps(getdata(url2),indent=4)
print(JSON)


# You should get output as something like
'''
    {
    "Specialty": "No Preservatives",
    "Weight": "85 Grams",
    "Ingredient Type": "Vegetarian",
    "Brand": "Kurkure",
    "Item package quantity": "1",
    "Package Information": "Pouch",
    "Manufacturer": "PepsiCo India Holdings Pvt. Ltd.N1 PepsiCo India Holdings Pvt. Ltd.",
    "Item part number": "100118049",
    "Net Quantity": "85.0 gram",
    "Product Dimensions": "5 x 18 x 29 cm; 85 Grams",
    "ASIN": "B004IF24XE",
    "Rating": "4.4",
    "Number of Reviews": "6,574",
    "Best Sellers Rank": "#53 in Grocery & Gourmet Foods , #1 in Namkeen",
    "Date First Available": "9 July 2020",
    "Item Weight": "85 g",
    "Item Dimensions LxWxH": "50 x 180 x 290 Millimeters"
}
'''

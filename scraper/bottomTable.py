import requests
from bs4 import BeautifulSoup
import re
import json

import unicodedata

def remove_unrendered_unicode(text):
    cleaned_text = ""
    for char in text:
        if unicodedata.category(char) != "Cf":
            cleaned_text += char
    return cleaned_text

def getdata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Technical details
    tech_spec_section = soup.select("#productDetails_techSpec_section_1")
    fields = tech_spec_section[0].select(".a-color-secondary.a-size-base.prodDetSectionEntry")
    values = tech_spec_section[0].select(".a-size-base.prodDetAttrValue")
    fields = [field.get_text(strip=True) for field in fields]
    values = [value.get_text(strip=True) for value in values]

    # Additional details
    detail_bullets_section = soup.select("#productDetails_detailBullets_sections1")
    rows = detail_bullets_section[0].select("tr")
    for row in rows:
        if row.find("th").get_text(strip=True) == "Customer Reviews":
            fields.append("Rating")
            values.append(row.find("td").select_one(".a-size-base.a-color-base").get_text(strip=True))
            fields.append("Number of Reviews")
            values.append(row.find("td").select_one("#acrCustomerReviewText").get_text(strip=True).split(" ")[0])
            continue
        if row.find("th").get_text(strip=True) == "Best Sellers Rank":
            fields.append(row.find("th").get_text(strip=True))
            text = row.find("td").get_text(strip=True)
            text = re.sub(r'\([^()]*\)', '', text).replace('\n', ', ')
            values.append(text)
            continue
        fields.append(row.find("th").get_text(strip=True))
        values.append(row.find("td").get_text(strip=True))

    n = len(fields)
    res = {}
    for i in range(n):
        fields[i] = remove_unrendered_unicode(fields[i])
        values[i] = remove_unrendered_unicode(values[i])
        res[fields[i]] = values[i]

    return res


# code to run and test
if __name__=="__main__":
    url="https://www.amazon.in/HP-Multi-Device-Bluetooth-Resistant-Auto-Detection/dp/B0BR3YKQQ1/ref=sr_1_2_sspa?keywords=keyboards&qid=1687188204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    url2="https://www.amazon.in/Kurkure-Namkeen-Masala-Munch-95g/dp/B004IF24XE/ref=sr_1_1?keywords=kurkure&qid=1687195614&sr=8-1"
    JSON=json.dumps(getdata(url),indent=4)
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

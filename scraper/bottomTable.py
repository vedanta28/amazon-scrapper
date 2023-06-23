import requests
from bs4 import BeautifulSoup
import re
import json

import unicodedata

from string import punctuation

def convert_to_lowercase_with_underscore(string):
    translator = str.maketrans("", "", punctuation)  # Create a translator to remove punctuation
    string = string.translate(translator)  # Remove punctuation marks
    words = string.split()  # Split the string into individual words
    lowercase_words = [word.lower() for word in words]  # Convert each word to lowercase
    result = '_'.join(lowercase_words)  # Join the lowercase words with underscores
    return result

def remove_unrendered_unicode(text):
    cleaned_text = ""
    for char in text:
        if unicodedata.category(char) != "Cf":
            cleaned_text += char
    return cleaned_text


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

def getdata(soup):
    

    fields = []
    values = []
    try:
        # Technical details
        tech_spec_section = soup.select(".a-keyvalue.prodDetTable")
        print(tech_spec_section)
        fields = tech_spec_section[0].select("th",{"class":"a-color-secondary a-size-base prodDetSectionEntry"})
        values = tech_spec_section[0].select("td",{"class":"a-size-base.prodDetAttrValue"})
        fields = [field.get_text(strip=True) for field in fields]
        values = [value.get_text(strip=True) for value in values]
    except:
        pass    

    try:
        # Additional details
        detail_bullets_section = soup.select("#productDetails_detailBullets_sections1")
        rows = detail_bullets_section[0].select("tr")
        for row in rows:
            if row.find("th").get_text(strip=True) == "Customer Reviews":
                fields.append("Rating")
                values.append(row.find("td").select_one(".a-size-base.a-color-base").get_text(strip=True))
                fields.append("Ratings")
                values.append(row.find("td").select_one("#acrCustomerReviewText").get_text(strip=True).split(" ")[0])
                continue
            if row.find("th").get_text(strip=True) == "Best Sellers Rank":
                fields.append("Ranking")
                text = row.find("td").get_text(strip=True)
                text = re.sub(r'\([^()]*\)', '', text).replace('\n', ', ')
                values.append(text)
                continue
            fields.append(row.find("th").get_text(strip=True))
            values.append(row.find("td").get_text(strip=True))
    except:
        pass

    try:
        ul_section = soup.select(".a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list")
        # since this might have some newlines and : and spaces in the text, we need to clean it
        for li in ul_section[0].select("li"):
            fields.append(li.get_text(strip=True).replace('\n','').split(":")[0].strip())
            values.append(li.get_text(strip=True).replace('\n','').split(":")[1].strip())
        txt=ul_section[1].get_text(strip=True).split(":")[0].strip()
        if txt=="Best Sellers Rank":
            fields.append(txt)
            values.append(ul_section[1].get_text(strip=True).split(":")[1].strip())

    except:
        pass

    print(fields)
    print(values)
    n = len(fields)
    k = len(values)
    print(n,k)
    res = {}
    for i in range(n):
        fields[i] = convert_to_lowercase_with_underscore(remove_unrendered_unicode(fields[i]))
        values[i] = remove_unrendered_unicode(values[i])
        res[fields[i]] = values[i]
    
    if "best_sellers_rank" in res:
        res["ranking"] = res["best_sellers_rank"]
        del res["best_sellers_rank"]

    return res


# code to run and test
if __name__=="__main__":
    url="https://www.amazon.in/HP-Multi-Device-Bluetooth-Resistant-Auto-Detection/dp/B0BR3YKQQ1/ref=sr_1_2_sspa?keywords=keyboards&qid=1687188204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    url2="https://www.amazon.in/Kurkure-Namkeen-Masala-Munch-95g/dp/B004IF24XE/ref=sr_1_1?keywords=kurkure&qid=1687195614&sr=8-1"
    url3="https://www.amazon.in/MASERATI-Stile-42-Mens-Watch/dp/B08X15J8MT?ref_=Oct_DLandingS_D_3994573e_10"
    url4="https://www.amazon.in/dp/B07YT1GKKH/ref=va_live_carousel?pf_rd_r=4P99QCREQ27DT52EWCPY&pf_rd_p=76ec0da0-3e09-4230-87db-2d8c9ab9db44&pf_rd_m=A21TJRUUN4KGV&pf_rd_t=Gateway&pf_rd_i=desktop&pf_rd_s=desktop-6&pd_rd_i=B07YT1GKKH&th=1&psc=1"
    url5="https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo1NjU0NjYzMTU0OTQ5ODE3OjE2ODc0NDQwNDA6c3BfYnRmOjIwMTY1MjE2Njk4ODk4OjowOjo&url=%2Fhelix-Digital-Black-Unisex-Watch-TW0HXW604T%2Fdp%2FB0BC5R5CTN%2Fref%3Dsr_1_60_sspa%3Fcrid%3D2VPH6RSQ6GEQH%26keywords%3Dwatches%26qid%3D1687444040%26sprefix%3Dwatche%252Caps%252C245%26sr%3D8-60-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9idGY%26psc%3D1"
    response = requests.get(url5, headers=headers)
    with open('output.html', 'w') as file:
        file.write(response.text)
        print('HTML content has been written to output.html')
    soup = BeautifulSoup(response.text,  "lxml")
    JSON=json.dumps(getdata(soup),indent=4)
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

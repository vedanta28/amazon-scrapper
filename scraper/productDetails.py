import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

def getDetails(centralCol, rightCol) -> dict: 
    try:
        title = centralCol.find("span", attrs={"id":'productTitle'}).text.strip()
    except AttributeError:
        title = ""

    try:
        savings = centralCol.find("span", attrs={"class":'savingsPercentage'}).text.strip().split("-")[1]
    except AttributeError:
        savings = "0%"
    
    try:
        sellingPrice = centralCol.find("span", attrs={"class":'priceToPay'}).find("span", attrs={"class": "a-offscreen"}).text.strip().split("₹")[1].replace(',', '')
    except AttributeError:
        sellingPrice = ""
    
    try:
        MRP = centralCol.find("span", attrs={"data-a-strike":'true'}).find("span", attrs={"class": "a-offscreen"}).text.strip().split("₹")[1].replace(',', '')
    except AttributeError:
        MRP = ""
    
    try:
        deal_type = centralCol.find("span", attrs={"class":'dealBadge'}).text.strip()
        isDOTD = (deal_type == "Deal of the Day")
        isDeal = (deal_type == "Deal" or deal_type == "Limited time deal")  
        isLD = (deal_type == "Lightning Deal")  
    except:
        isDOTD = False
        isDeal = False
        isLD = False
    
    try:
        ratingsCount = centralCol.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip().split(" ")[0]
    except AttributeError:
        ratingsCount = ""
    
    try:
        ratings = centralCol.find("span", attrs={"id":'acrPopover'}).text.strip().split(" ")[0]
    except AttributeError:
        ratings = ""
    
    try:
        soldBy = rightCol.find("div", attrs={"id":'merchant-info'}).text.strip().split("and")[0].split(" ")[2]
    except AttributeError:
        soldBy = ""
    
    try:
        availability = rightCol.find("div", attrs={"id":'availability'}).text.strip()
    except AttributeError:
        availability = ""

    ProductDetails = {
        "title": title,
        "savings": savings,
        "sellingPrice": sellingPrice,
        "MRP": MRP,
        "isDOTD": isDOTD,
        "isDeal": isDeal,
        "isLD": isLD,
        "ratingsCount": ratingsCount,
        "ratings": ratings,
        "availability": availability,
        "soldBy": soldBy
    }

    return ProductDetails


# url = input("Enter the URL of the product: ")
url = 'https://www.amazon.in/Google-Pixel-Watch-Smartwatch-Stainless/dp/B0BGX1CSRY/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=RssbX&content-id=amzn1.sym.cd312cd6-6969-4220-8ac7-6dc7c0447352&pf_rd_p=cd312cd6-6969-4220-8ac7-6dc7c0447352&pf_rd_r=M858G1PBZCM3TN2XAX1S&pd_rd_wg=iz97E&pd_rd_r=81cf11f5-6691-4f62-b21b-55fa18807c2f&pd_rd_i=B0BGX1CSRY'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

if __name__ == '__main__':    
    
    print("Loading URL...")
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    centralCol = soup.find("div", attrs={"id":'centerCol'})
    rightCol = soup.find("div", attrs={"id":'rightCol'})

    ProductDetails = getDetails(centralCol, rightCol)
    save_name = f"ProductDetails_{datetime.now().strftime('%Y-%m-%d-%f')}.json"
    with open(save_name, 'w') as json_file:
        json.dump(ProductDetails, json_file, indent=4)

    print("Product Details saved to", save_name)
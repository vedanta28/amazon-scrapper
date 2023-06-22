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
        selling_price = centralCol.find("span", attrs={"class":'priceToPay'}).find("span", attrs={"class": "a-offscreen"}).text.strip().replace(',', '')[1:]
    except AttributeError:
        selling_price = ""
    
    try:
        MRP = centralCol.find("span", attrs={"data-a-strike":'true'}).find("span", attrs={"class": "a-offscreen"}).text.strip().replace(',', '')[1:]
    except AttributeError:
        MRP = selling_price
    
    try:
        deal_type = centralCol.find("span", attrs={"class":'dealBadge'}).text.strip()
        isDOTD = (deal_type == "Deal of the Day")
        isDeal = (deal_type == "Deal" or deal_type == "Limited time deal")  
    except:
        isDOTD = False
        isDeal = False
    
    try:
        ratings_count = centralCol.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip().split(" ")[0]
    except AttributeError:
        ratings_count = ""
    
    try:
        ratings = centralCol.find("span", attrs={"id":'acrPopover'}).text.strip().split(" ")[0]
    except AttributeError:
        ratings = ""
    
    try:
        merchantInfo = rightCol.find("div", attrs={"id":'merchant-info'}).text.strip()
        
        if 'Sold and fulfilled by ' in merchantInfo:
            sold_by = merchantInfo.split("Sold and fulfilled by ")[1]

        elif 'Sold and delivered by ' in merchantInfo:
            sold_by = merchantInfo.split("Sold and delivered by ")[1]

        elif 'Sold and Fulfilled by ' in merchantInfo:
            sold_by = merchantInfo.split("Sold and Fulfilled by ")[1]

        elif 'Sold and Delivered by ' in merchantInfo:
            sold_by = merchantInfo.split("Sold and Delivered by ")[1]

        elif 'Sold by' in merchantInfo:
            if ' and Fulfilled by ' in merchantInfo:
                sold_by = merchantInfo.split(" and Fulfilled by ")[0].split("Sold by ")[1]
            elif ' and Delivered by ' in merchantInfo:
                sold_by = merchantInfo.split(" and Delivered by ")[0].split("Sold by ")[1]
            else:
                sold_by = merchantInfo.split(" and ")[0].split("Sold by ")[1]

        else:
            sold_by = merchantInfo.split(" and ")[0].split("Sold by ")[1]
            
        delivery_type = "MFN"
        if 'Fulfilled by Amazon' in merchantInfo:
            delivery_type = "FBA"

    except AttributeError:
        sold_by = ""
        delivery_type = ""
        
    try:
        shipping_fees = "0"
        shipment = rightCol.find("div", attrs={"id": 'deliveryBlockMessage'}).text.strip()
        if 'FREE' in shipment:
            shipping_fees = "0"
        else:
            shipping_fees = shipment.split(" delivery")[0][1:]
    except AttributeError:
        shipping_fees = ""

    try:
        availability = rightCol.find("div", attrs={"id":'availability'}).text.strip()
    except AttributeError:
        if rightCol.text.count("Currently unavailable"):
            availability = "Currently unavailable"
        elif rightCol.text.count("Temporarily unavailable"):
            availability = "Temporarily unavailable"
        else:
            availability = ""
    
    isLD = False
    if( rightCol.text.count("Lightning") ):
        isLD = True
        try:
            selling_price = centralCol.find("span", attrs={"class":'apexPriceToPay'}).text.strip().split("₹")[1]
            save_text = rightCol.find("div", attrs={"id": 'corePrice_feature_div'}).text.strip()
            save_index = save_text.find("%")
            savings = save_text[save_index-2:save_index].strip()
        except AttributeError:
            selling_price = ""
            savings = ""

    ProductDetails = {
        "title": title,
        "savings": savings,
        "selling_price": selling_price,
        "MRP": MRP,
        "isDOTD": isDOTD,
        "isDeal": isDeal,
        "isLD" : isLD,
        "ratings_count": ratings_count,
        "ratings": ratings,
        "availability": availability,
        "sold_by": sold_by,
        "delivery_type": delivery_type,
        "shipping_fees": shipping_fees
    }

    return ProductDetails

# url = 'https://www.amazon.in/Google-Pixel-Watch-Smartwatch-Stainless/dp/B0BGX1CSRY/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=RssbX&content-id=amzn1.sym.cd312cd6-6969-4220-8ac7-6dc7c0447352&pf_rd_p=cd312cd6-6969-4220-8ac7-6dc7c0447352&pf_rd_r=M858G1PBZCM3TN2XAX1S&pd_rd_wg=iz97E&pd_rd_r=81cf11f5-6691-4f62-b21b-55fa18807c2f&pd_rd_i=B0BGX1CSRY'
url = 'https://www.amazon.in/Shalimar-Premium-Garbage-Medium-Rolls/dp/B07KT9Q54M?pf_rd_r=HWP7MV1MKY0DKAEFATYV&pf_rd_t=Events&pf_rd_i=deals&pf_rd_p=5e777f37-e648-40d9-b6df-497b635b786d&pf_rd_s=slot-15&ref=dlx_deals_gd_dcl_img_1_390c2a2c_dt_sl15_6d&th=1'
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
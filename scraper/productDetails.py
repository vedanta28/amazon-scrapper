from bs4 import BeautifulSoup
import json
import requests

class AmazonProductDetailsScraper:

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def get_product_name(self, soup_object: BeautifulSoup) -> str:
        try:
            product_name = soup_object.find("span", attrs={"id":'productTitle'}).text.strip()
        except AttributeError:
            product_name = ""
        return product_name
           
    def get_price(self, soup_object: BeautifulSoup) -> str:
        try:
            price = soup_object.find("span", attrs={"class":'priceToPay'}).find("span", attrs={"class": "a-offscreen"}).text.strip().replace(',', '')[1:]
        except AttributeError:
            try:
                # price = soup_object.find("span", attrs={"class":'a-price a-text-price a-size-medium apexPriceToPay'}).span.text.strip()
                price = ""
                prices = soup_object.find_all("span", attrs={"class":'a-price a-text-price a-size-medium apexPriceToPay'})
                for i, p in enumerate(prices):
                    if i != 0:
                        price += " - "
                    price += p.span.text.strip()
            except AttributeError:
                price = ""
        return price

    def get_mrp(self, soup_object: BeautifulSoup) -> str:
        try:
            mrp = soup_object.find("span", attrs={"data-a-strike":'true'}).find("span", attrs={"class": "a-offscreen"}).text.strip().replace(',', '')[1:]
        except AttributeError:
            mrp = ""
        return mrp

    def get_rating(self, soup_object: BeautifulSoup) -> str:
        try:
            rating = soup_object.find("span", attrs={"id":'acrPopover'}).text.strip().split(" ")[0]
        except AttributeError:
            rating = ""
        return rating

    def get_ratings_count(self, soup_object: BeautifulSoup) -> str:
        try:
            ratings_count = soup_object.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip().split(" ")[0].replace(",","")
        except AttributeError:
            ratings_count = ""
        return ratings_count 
    
    def get_shipping_fee(self, soup_object: BeautifulSoup) -> str:
        try:
            shipping_fee = "0"
            shipment = soup_object.find("div", attrs={"id": 'deliveryBlockMessage'}).text.strip()
            if 'FREE' in shipment:
                shipping_fee = "0"
            else:
                shipping_fee = shipment.split(" delivery")[0][1:]
        except AttributeError:
            shipping_fee = ""
        return shipping_fee
    
    def get_status(self, soup_object: BeautifulSoup) -> str:
        status = ""
        try:
            status = soup_object.find("div", attrs={"id":'availability'}).text.strip()
        except AttributeError:
            try:
                if soup_object.text.count("Currently unavailable"):
                    status = "Currently unavailable"
                elif soup_object.text.count("Temporarily unavailable"):
                    status = "Temporarily unavailable"
            except AttributeError:
                status = ""
        return status
    
    def get_deal_type(self, soup_object: BeautifulSoup) -> list:
        try:
            deal_type = soup_object.find("span", attrs={"class":'dealBadge'}).text.strip()
            is_dotd = (deal_type == "Deal of the Day")   
            is_deal = (deal_type == "Deal" or deal_type == "Limited time deal")
        except:
            is_dotd = False
            is_deal = False
        return [is_dotd, is_deal]
    
    def get_merchant_info(self, soup_object: BeautifulSoup) -> list:
        try:
            merchantInfo = soup_object.find("div", attrs={"id":'merchant-info'}).text.strip()
            delivery_type = "MFN"
            if 'Fulfilled by Amazon' in merchantInfo:
                delivery_type = "FBA"
        
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
        except AttributeError:
            sold_by = ""
            delivery_type = ""
        return [sold_by, delivery_type]


    def scrape_product_details(self):
        self.centralCol = self.soup.find("div", attrs={"id":'centerCol'})
        self.rightCol = self.soup.find("div", attrs={"id":'rightCol'})
        isLD = False
        try:
            price = self.get_price(self.centralCol)
            if( self.rightCol.text.count("Lightning") and price == ""):
                isLD = True
                price = self.centralCol.find("span", attrs={"class":'apexPriceToPay'}).text.strip().split("₹")[1]
        except AttributeError:
            price = ""
        
        deal_type = self.get_deal_type(self.centralCol)
        merchant_info = self.get_merchant_info(self.rightCol)

        ProductDetails = {
            "product_name": self.get_product_name(self.centralCol),
            "price": price,
            "mrp": self.get_mrp(self.centralCol),
            "is_dotd": deal_type[0],
            "is_deal": deal_type[1],
            "is_ld" : isLD,
            "ratings_count": self.get_ratings_count(self.centralCol),
            "rating": self.get_rating(self.centralCol),
            "status": self.get_status(self.rightCol),
            "sold_by": merchant_info[0],
            "fba/mfn": merchant_info[1],
            "shipping_fee": self.get_shipping_fee(self.rightCol)
        }

        return ProductDetails

if __name__ == '__main__':
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
    
    url = 'https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo1NjU0NjYzMTU0OTQ5ODE3OjE2ODc0NDQwNDA6c3BfYXRmOjIwMTM2NzA3MzYwNzk4OjowOjo&url=%2FTimex-Analog-Blue-Dial-Watch-TW00ZR262E%2Fdp%2FB07H3K85H5%2Fref%3Dsr_1_1_sspa%3Fcrid%3D2VPH6RSQ6GEQH%26keywords%3Dwatches%26qid%3D1687444040%26sprefix%3Dwatche%252Caps%252C245%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,  "lxml")
    data0 = AmazonProductDetailsScraper(soup).scrape_product_details()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data0, f, ensure_ascii=False, indent=4)
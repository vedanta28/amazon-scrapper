from bs4 import BeautifulSoup

class Product_Details_Scraper:

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
            ratings = soup_object.find("span", attrs={"id":'acrPopover'}).text.strip().split(" ")[0]
        except AttributeError:
            ratings = ""
        return ratings

    def get_ratings_count(self, soup_object: BeautifulSoup) -> str:
        try:
            ratings_count = soup_object.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip().split(" ")[0]
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
        try:
            status = soup_object.find("div", attrs={"id":'availability'}).text.strip()
        except AttributeError:
            if soup_object.text.count("Currently unavailable"):
                status = "Currently unavailable"
            elif soup_object.text.count("Temporarily unavailable"):
                status = "Temporarily unavailable"
            else:
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

        try:
            isLD = False
            price = self.get_price(self.centralCol)
            if( self.rightCol.text.count("Lightning") ):
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
            "rating": self.get_rating(self.get_rating),
            "status": self.get_status(self.rightCol),
            "sold_by": merchant_info[0],
            "fba/mfn": merchant_info[1],
            "shipping_fee": self.get_shipping_fee(self.rightCol)
        }

        return ProductDetails
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

# Get your own user agent at:
# https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

class Review:
    def __init__(self, username, rating, title, country, date, product_variant, is_verified, review_body, found_helpful):
        self.username = username
        self.rating = rating
        self.title = title
        self.country = country
        self.date = date
        self.product_variant = product_variant
        self.is_verified = is_verified
        self.review_body = review_body
        self.found_helpful = found_helpful

def get_username(soup):
    try:
        username = soup.find("span", attrs={"class":'a-profile-name'}).text
    except:
        username = ""
    return username
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={"data-hook":'review-star-rating'}).span.text.split()[0]
    except:
        rating = ""
    return rating
def get_title(soup):
    try:
        title = soup.find("a", attrs={"data-hook":'review-title'}).find_all('span')[-1].text
    except:
        title = ""
    return title
def get_country_and_date(soup):
    try:
        string = soup.find("span", attrs={"data-hook":'review-date'}).text
        country = re.search(r'Reviewed in (.+?) on', string).group(1)
        date_match = re.search(r'on (\d+ \w+ \d+)', string).group(1)
        date = datetime.strptime(date_match, "%d %B %Y").strftime("%d/%m/%Y")
    except:
        country = ""
        date = ""
    return country, date
def get_product_variant(soup):
    try:
        product_variant = soup.find("a", attrs={"data-hook":'format-strip'}).text
    except:
        product_variant = ""
    return product_variant
def get_verified(soup):
    try:
        is_verified = soup.find("span", attrs={"data-hook":'avp-badge'}).text
    except:
        is_verified = ""
    if is_verified == "Verified Purchase":
        return True
    else:
        return False
def get_review_body(soup):
    try:
        review_body = soup.find("span", attrs={"data-hook":'review-body'}).span.text
    except:
        review_body = ""
    return review_body
def get_found_helpful(soup):
    try:
        found_helpful = soup.find("span", attrs={"data-hook":'helpful-vote-statement'}).text.split()[0]
    except:
        found_helpful = ""
    return found_helpful


# Initialize an empty array of Review instances
reviews_list = []

def get_reviews_from_page(url):
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    reviews = soup.find_all("div", attrs={"class":'a-section review aok-relative'})
    for review in reviews:
        username = get_username(soup=review)
        rating = get_rating(soup=review)
        title = get_title(soup=review)
        country, date = get_country_and_date(soup=review)
        product_variant = get_product_variant(soup=review)
        is_verified = get_verified(soup=review)
        review_body = get_review_body(soup=review)
        found_helpful = get_found_helpful(soup=review)
        review_instance = Review(username, rating, title, country, date, product_variant, is_verified, review_body, found_helpful)
        reviews_list.append(review_instance)

if __name__ == '__main__':

    url = 'https://www.amazon.in/Harissons-Sirius-Laptop-Backpacks-Built/product-reviews/B07MD1G8RZ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    url2 = 'https://www.amazon.in/Harissons-Sirius-Laptop-Backpacks-Built/product-reviews/B07MD1G8RZ/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2'

    get_reviews_from_page(url)
    for review in reviews_list:
        print("Username:", review.username)
        print("Rating:", review.rating)
        print("Title:", review.title)
        print("Country:", review.country)
        print("Date:", review.date)
        print("Product Variant:", review.product_variant)
        print("Is Verified:", review.is_verified)
        print("Review Body:", review.review_body)
        print("Found Helpful:", review.found_helpful)
        print()





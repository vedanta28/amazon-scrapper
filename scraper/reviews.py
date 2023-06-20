import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

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

URLS = [
    "https://www.amazon.in/dp/product-reviews/B07MD1G8RZ?pageNumber=2"
]


def get_page_html(page_url: str) -> str:
    resp = requests.get(page_url, headers=headers)
    return resp.text


def get_reviews_from_html(page_html: str) -> BeautifulSoup:
    soup = BeautifulSoup(page_html, "lxml")
    reviews = soup.find_all("div", {"class": "a-section celwidget"})
    return reviews


def get_review_date(soup_object: BeautifulSoup):
    date_string = soup_object.find("span", {"class": "review-date"}).get_text()
    date_match = re.search(r'on (\d+ \w+ \d+)', date_string).group(1)
    date = datetime.strptime(date_match, "%d %B %Y").strftime("%d/%m/%Y")
    return date

def get_review_country(soup_object: BeautifulSoup):
    country = re.search(r'Reviewed in (.+?) on', soup_object.find("span", {"class": "review-date"}).get_text()).group(1)
    return country.split()[0]

def get_review_username(soup_object: BeautifulSoup) -> str:
    review_text = soup_object.find(
        "span", {"class": "a-profile-name"}
    ).get_text()
    return review_text.strip()

def get_review_text(soup_object: BeautifulSoup) -> str:
    review_text = soup_object.find(
        "span", {"class": "a-size-base review-text review-text-content"}
    ).get_text()
    return review_text.strip()


def get_review_header(soup_object: BeautifulSoup) -> str:
    review_header = soup_object.find(
        "a",
        {
            "class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"
        },
    ).find_all('span')[-1].get_text()
    return review_header.strip()


def get_number_stars(soup_object: BeautifulSoup) -> str:
    stars = soup_object.find("span", {"class": "a-icon-alt"}).get_text().split()[0]
    return stars.strip()


def get_product_variant(soup_object: BeautifulSoup) -> str:
    product = soup_object.find(
        "a", {"class": "a-size-mini a-link-normal a-color-secondary"}
    ).get_text()
    return product.strip()

def get_verified(soup_object: BeautifulSoup) -> bool:
    try:
        is_verified = soup_object.find(
            "span", attrs={"data-hook":'avp-badge'}
        ).get_text()
    except:
        is_verified = ""
    if is_verified == "Verified Purchase":
        return True
    else:
        return False

def get_found_helpful(soup_object: BeautifulSoup) -> str:
    try:
        found_helpful = soup_object.find(
            "span", attrs={"data-hook":'helpful-vote-statement'}
        ).get_text().split()[0]
    except:
        found_helpful = ""
    return found_helpful


def orchestrate_data_gathering(single_review: BeautifulSoup) -> dict:
    return {
        "review_username": get_review_username(single_review),
        "review_stars": get_number_stars(single_review),
        "review_title": get_review_header(single_review),
        "review_country": get_review_country(single_review),
        "review_date": get_review_date(single_review),
        "review_product_variant": get_product_variant(single_review),
        "review_is_verified": get_verified(single_review),
        "review_text": get_review_text(single_review),
        "review_helpul": get_found_helpful(single_review),
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    all_results = []
    asin = 'B07MD1G8RZ'
    base_url = 'https://www.amazon.in/dp/product-reviews/' + asin

    num_pages = 100  # Define the number of pages you want to iterate over

    for page_number in range(1, num_pages + 1):
        url = base_url + f'?pageNumber={page_number}'
        logging.info(url)
        html = get_page_html(url)
        reviews = get_reviews_from_html(html)
        initial_length = len(all_results)
        for rev in reviews:
            data = orchestrate_data_gathering(rev)
            all_results.append(data)
        if len(all_results) == initial_length:
            break

    save_name = f"{asin}_{datetime.now().strftime('%Y-%m-%d-%m')}.json"
    with open(save_name, 'w') as json_file:
        json.dump(all_results, json_file, indent=4)

    logging.info(f"{len(all_results)} is the length of the list")
    logging.info(f"Saved to {save_name}")
    logging.info('Done yayy')

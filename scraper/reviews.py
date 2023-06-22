import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

class AmazonReviewScraper:
    def __init__(self):
        self.headers = {
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

    def get_page_html(self, page_url: str) -> str:
        resp = requests.get(page_url, headers=self.headers)
        return resp.text

    def get_reviews_from_html(self, page_html: str) -> BeautifulSoup:
        soup = BeautifulSoup(page_html, "lxml")
        reviews = soup.find_all("div", {"class": "a-section celwidget"})
        return reviews

    def get_review_date(self, soup_object: BeautifulSoup):
        try:
            date_string = soup_object.find("span", {"class": "review-date"}).get_text()
            date_match = re.search(r'on (\d+ \w+ \d+)', date_string).group(1)
            date = datetime.strptime(date_match, "%d %B %Y").strftime("%d/%m/%Y")
        except:
            date = ""
        return date

    def get_review_country(self, soup_object: BeautifulSoup):
        try:
            country = re.search(r'Reviewed in (.+?) on', soup_object.find("span", {"class": "review-date"}).get_text()).group(1).split()[0]
        except:
            country = ""
        return country

    def get_review_username(self, soup_object: BeautifulSoup) -> str:
        try:
            review_text = soup_object.find(
                "span", {"class": "a-profile-name"}
            ).get_text().strip()
        except:
            review_text = ""
        return review_text

    def get_review_text(self, soup_object: BeautifulSoup) -> str:
        try:
            review_text = soup_object.find(
                "span", {"class": "a-size-base review-text review-text-content"}
            ).get_text().strip()
        except:
            review_text = ""
        return review_text

    def get_review_header(self, soup_object: BeautifulSoup) -> str:
        try:
            review_header = soup_object.find(
                "a",
                {
                    "class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"
                },
            ).find_all('span')[-1].get_text().strip()
        except:
            review_header = ""
        return review_header

    def get_number_stars(self, soup_object: BeautifulSoup) -> str:
        try:
            stars = soup_object.find(
                "span", {"class": "a-icon-alt"}
            ).get_text().split()[0].strip()
        except:
            stars = ""
        return stars

    def get_product_variant(self, soup_object: BeautifulSoup) -> str:
        try:
            product = soup_object.find(
                "a", {"class": "a-size-mini a-link-normal a-color-secondary"}
            ).get_text()
        except:
            product = ""
        return product.strip()

    def get_verified(self, soup_object: BeautifulSoup) -> bool:
        try:
            is_verified = soup_object.find(
                "span", attrs={"data-hook": 'avp-badge'}
            ).get_text()
        except:
            is_verified = ""
        if is_verified == "Verified Purchase":
            return True
        else:
            return False

    def get_found_helpful(self, soup_object: BeautifulSoup) -> str:
        try:
            found_helpful = soup_object.find(
                "span", attrs={"data-hook": 'helpful-vote-statement'}
            ).get_text().split()[0]
        except:
            found_helpful = ""
        return found_helpful

    def orchestrate_data_gathering(self, single_review: BeautifulSoup) -> dict:
        return {
            "review_username": self.get_review_username(single_review),
            "review_stars": self.get_number_stars(single_review),
            "review_title": self.get_review_header(single_review),
            "review_country": self.get_review_country(single_review),
            "review_date": self.get_review_date(single_review),
            "review_product_variant": self.get_product_variant(single_review),
            "review_is_verified": self.get_verified(single_review),
            "review_text": self.get_review_text(single_review),
            "review_helpful": self.get_found_helpful(single_review),
        }

    def scrape_reviews(self, asin: str, num_pages: int):
        all_results = []
        base_url = 'https://www.amazon.in/dp/product-reviews/' + asin

        for page_number in range(1, num_pages + 1):
            url = base_url + f'?pageNumber={page_number}'
            logging.info(url)
            html = self.get_page_html(url)
            reviews = self.get_reviews_from_html(html)
            initial_length = len(all_results)
            for rev in reviews:
                data = self.orchestrate_data_gathering(rev)
                all_results.append(data)
            if len(all_results) == initial_length:
                break

        save_name = f"{asin}_{datetime.now().strftime('%Y-%m-%d-%m')}_reviews.csv"

        if all_results:
            with open(save_name, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=all_results[0].keys())
                writer.writeheader()
                writer.writerows(all_results)

            logging.info(f"{len(all_results)} is the length of the list")
            logging.info(f"Saved to {save_name}")
        else:
            logging.warning("No results found. Nothing to save.")

        logging.info('Done yayy')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scraper = AmazonReviewScraper()
    scraper.scrape_reviews(asin='B094DP3177', num_pages=100)

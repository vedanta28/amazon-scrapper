from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

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




if __name__ == '__main__':
    # Get your own user agent at:
    # https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

    url = 'https://www.amazon.in/OnePlus-Wireless-Earbuds-Titanium-Playback/product-reviews/B0BYJ6ZMTS/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'


    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    review = soup.find("div", attrs={"class":'a-section review aok-relative'})
    username = get_username(soup=review)
    rating = get_rating(soup=review)
    title = get_title(soup=review)
    country, date = get_country_and_date(soup=review)

    print(f'Username: {username}')
    print(f'Rating: {rating}')
    print(f'Title: {title}')
    print(f'Country: {country}')
    print(f'Date: {date}')



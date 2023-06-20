from bs4 import BeautifulSoup
import requests

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":'productTitle'}).text.strip()
    except AttributeError:
        title = ""
    return title
def get_MRP(soup):
    try:
        MRP = soup.find("span", attrs={"class":'a-price a-text-price a-size-base'}).span.text
    except AttributeError:
        try:
            MRP = soup.find("span", attrs={"class":'a-price a-text-price'}).span.text
        except AttributeError:
            MRP = ""
    return MRP
def get_rating(soup):
    try:
        rating = rating_section.find("span", attrs={"class":'a-size-base a-color-base'}).text.strip()
    except AttributeError:
        rating = ""
    return rating
def get_rating_cnt(soup):
    try:
        rating_cnt = rating_section.find("span", attrs={"id":'acrCustomerReviewText'}).string.split()[0]
    except AttributeError:
        rating_cnt = ""
    return rating_cnt
        








if __name__ == '__main__':
    # Get your own user agent at:
    # https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Accept-Language': 'en-US, en;q=0.5'}

    url = 'https://www.amazon.in/WONDERLAND-FOODS-DEVICE-Raisins-Kishmish/dp/B08VGDWJRM?ref_=Oct_DLandingS_D_07408eea_0&th=1'

    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    centreCol = soup.find("div", attrs={"class":'centerColAlign'})
    title = get_title(soup=centreCol)
    MRP = get_MRP(soup=centreCol)

    rating_section = soup.find("div", attrs={"id":'averageCustomerReviews'})
    rating = get_rating(rating_section)
    rating_cnt = get_rating_cnt(rating_section)

    print(f'Title: {title}')
    print(f'MRP: {MRP}')
    print(f'Rating: {rating}')
    print(f'Rating Count: {rating_cnt}')
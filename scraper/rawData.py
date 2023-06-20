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

    url = 'https://www.amazon.in/Google-Pixel-Watch-Smartwatch-Stainless/dp/B0BGX1CSRY/?_encoding=UTF8&pd_rd_w=LBGmG&content-id=amzn1.sym.22a42d01-0089-4fec-a28b-ec7a361d085f&pf_rd_p=22a42d01-0089-4fec-a28b-ec7a361d085f&pf_rd_r=SW9VRSHH498801RDM1D6&pd_rd_wg=s4ruc&pd_rd_r=2e473a06-c62f-4a99-a028-831e575b28bb&ref_=pd_gw_ci_mcx_mr_hp_d'

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
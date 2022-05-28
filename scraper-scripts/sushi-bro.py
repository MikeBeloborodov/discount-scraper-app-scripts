from bs4 import BeautifulSoup as bs
from typing import List
import utils
import os
from dotenv import load_dotenv
import re


def get_data(html_data: str) -> List[str]:
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='product-wrapper')
    phone_number = ""
    for element in (soup.find(name='ul', 
                                attrs='inline-list inline-list-with-border main-nav-style')
                                .find_all(name='a')):
        try:
            phone_number = element.get("href")[3:]
        except:
            pass

    sushi_set_data = []
    for element in elements:
        data = {}
        try:
            # title
            data.update({"title": element.h3.a.string})
            
            # weight
            product_info = element.find(name='div', attrs="product-information")
            weight_raw = product_info.find(name='div', attrs='hover-content-inner').text
            weight_clean = re.findall('Вес:[\s0-9]*', weight_raw)[0][5:]
            data.update({"weight": weight_clean + 'гр'})
            
            # prices
            prices = element.find_all(name='span', attrs='woocommerce-Price-amount amount')
            if len(prices) == 2:
                data.update({"old_price": f"{str(prices[0].text)[:-5]} руб"})
                data.update({"new_price": f"{str(prices[1].text)[:-5]} руб"})
            else:
                data.update({"new_price": f"{str(prices[0].text)[:-5]} руб"})
            
            # img
            data.update({"img": element.img.get('src')})

            # link
            data.update({"link": element.a.get('href')})
            
            # phone number
            data.update({"phone_number": phone_number})
            sushi_set_data.append(data)
        except Exception as error:
            print(error)

    return sushi_set_data

def main():
    load_dotenv()

    URL = os.getenv('URL_SUSHI_BRO')
    FILE_NAME = os.getenv('FILE_NAME_SUSHI_BRO')
    html_data_new = ""
    html_data_old = ""

    html_data_new = utils.get_html_page(URL, FILE_NAME)

    if os.path.exists(FILE_NAME + ".html"):
        with open(FILE_NAME + ".html", "r") as file:
            html_data_old = file.read()

    sushi_bro_new_data = get_data(html_data_old)
    sushi_bro_old_data = get_data(html_data_old)

    if sushi_bro_new_data == sushi_bro_old_data:
        print(sushi_bro_new_data)
        print(len(sushi_bro_new_data))
        print("Up to date")
    else:
        with open(FILE_NAME + ".html", "w") as file:
            file.write(html_data_new)
        print(sushi_bro_new_data)
        # send data to api

if __name__ == "__main__":
    main()
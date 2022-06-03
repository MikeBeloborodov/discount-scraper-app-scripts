from bs4 import BeautifulSoup as bs
from typing import List
import utils
import os
from dotenv import load_dotenv
import re


def get_data(html_data: str, url: str) -> List[str]:
    if not html_data:
        return None
        
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='product-wrapper')
    phone_number = ""
    for element in (soup.find(name='ul', 
                                attrs='inline-list inline-list-with-border main-nav-style')
                                .find_all(name='a')):
        try:
            phone_number = element.get("href")[4:]
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

            # website link
            data.update({"website_link": url})

            # website title
            data.update({"website_title": "Суши бро"})

            # cathegory
            data.update({"cathegory": "sushi"})

            sushi_set_data.append(data)
        except Exception as error:
            print(error)

    return sushi_set_data

def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_SUSHI_BRO')
        FILE_NAME = os.getenv('FILE_NAME_SUSHI_BRO')

        html_data = utils.get_html_page(URL)
        sushi_bro_data = get_data(html_data, URL)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(sushi_bro_data)}")
        utils.save_json(sushi_bro_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occured: {error}")


if __name__ == "__main__":
    main()
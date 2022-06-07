from bs4 import BeautifulSoup as bs
from typing import List
import scraper_scripts.utils as utils
import os
from dotenv import load_dotenv
import re


def get_data(html_data: bytes) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception

    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='product-wrapper')
    phone_number = "+3412771176"
    
    sushi_set_data = []
    for element in elements:
        data = {}
        try:
            # title
            title_raw = element.h3
            if not title_raw:
                continue
            title_clean = element.h3.a.string
            data.update({"title": title_clean})

            # weight
            product_info = element.find(name='div', attrs="product-information")
            weight_raw = product_info.find(name='div', attrs='hover-content-inner').text
            weight_clean = re.findall('Вес:[\s0-9]*', weight_raw)[0][5:]
            data.update({"weight": weight_clean + 'гр'})
           
            # prices
            prices = element.find_all(name='span', attrs='woocommerce-Price-amount amount')
            if len(prices) == 2:
                data.update({"old_price": f"{str(prices[0].text)[:-5]}".replace(' ', '')})
                data.update({"new_price": f"{str(prices[1].text)[:-5]}".replace(' ', '')})
            else:
                data.update({"new_price": f"{str(prices[0].text)[:-5]}".replace(' ', '')})
            
            # img
            data.update({"img": element.img.get('src')})

            # link
            data.update({"link": element.a.get('href')})

            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({"website_link": URL})

            # website title
            data.update({"website_title": "Суши бро"})

            # weight
            weight_raw = element.find(name='div', attrs='hover-content-inner').text.strip()
            weight_clean = re.findall('.*\гр', weight_raw)
            data.update({'weight': weight_clean[0][5:-1]})

            # ingredients
            ingredients_raw = element.find(name='div', attrs='hover-content-inner').text.strip()
            ingredients_clean = re.findall('Состав:.*', ingredients_raw)
            if ingredients_clean:
                data.update({'ingredients': ingredients_clean[0][7:]})

            # category
            data.update({"category": "sushi"})
            sushi_set_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return sushi_set_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        sushi_bro_data = get_data(html_data)

        # utils.print_data(sushi_bro_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(sushi_bro_data)}")
        utils.save_json(sushi_bro_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")

    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_SUSHI_BRO')
    FILE_NAME = os.getenv('FILE_NAME_SUSHI_BRO')
    main()

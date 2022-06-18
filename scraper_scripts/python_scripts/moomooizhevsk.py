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
    burger_box = soup.find(name='div', attrs='menu-block item-section-burgery')
    elements = burger_box.find_all(name='div', attrs='product')
    phone_number_box = soup.find(name='div', attrs='top-desc-delivery')
    phone_number = phone_number_box.a.text.strip()

    burger_data = []

    for element in elements:
        data = {}
        try:
            # there is a class 'product stop' that we have to avoid
            if len(element['class']) > 1:
                continue

            # title
            title_raw = element.find(name='div', attrs='menu-item-description-main').text.strip()
            title_clean = re.findall('[А-я, A-z]+', title_raw)
            data.update({"title": title_clean[0]})
            
            # weight
            weight = element.find(name='span', attrs='weight-desc').text.strip()
            data.update({"weight": weight})
            
            # price
            price_raw = element.find(name='div', attrs='price').text.strip()
            price_clean = re.findall('\d+', price_raw.replace(" ", ""))
            data.update({"new_price": price_clean[0]})
            
            # img
            img = element.find(name='img', attrs='menu-item-img').get('src')
            data.update({"img": img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({"website_link": URL})

            # website title
            data.update({"website_title": "MooMooIzhevsk"})

            # ingredients
            ingredients = element.find(name='div', attrs='menu-item-description-add').text.strip()
            data.update({"ingredients": ingredients})

            # category
            data.update({"category": "burger"})

            burger_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return burger_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        moomooizhevsk_data = get_data(html_data)

        # utils.print_data(moomooizhevsk_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(moomooizhevsk_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(moomooizhevsk_data)}")
        utils.save_json(moomooizhevsk_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_MOOMOOIZHEVSK')
    FILE_NAME = os.getenv('FILE_NAME_MOOMOOIZHEVSK')
    main()


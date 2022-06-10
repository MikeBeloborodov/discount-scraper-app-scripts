from scraper_scripts import utils
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup as bs
from typing import List
import re


def get_single_pages_urls(html_data: bytes) -> list:
    if not html_data:
        print(f"[{FILE_NAME}] HTML DATA IS EMPTY!")
        raise Exception

    soup = bs(html_data, "html.parser")
    single_page_elements = soup.find_all(name="div", attrs='product-item__link')

    page_urls = []
    for element in single_page_elements:
        page_urls.append(element.a.get('href'))
    return page_urls


def get_kebab_data(single_pages_urls: list) -> List[dict]:
    if not single_pages_urls:
        print(f"[{FILE_NAME}] ERROR LOADING SINGLE PAGES!")
        raise Exception

    kebab_data = []
    for page in single_pages_urls:
        try:
            html_data = utils.get_html_page(page)

            soup = bs(html_data, "html.parser")
            kebab_box = soup.find(name='article', id='products-show')
            phone_number = soup.find(name='div', attrs='top-contacts__phones-item').text.strip()

            single_item_data = {}
            
           
            # title
            title = kebab_box.find(name='div', attrs='product__name show-for-medium').text.strip()
            single_item_data.update({"title": title})

            # img
            img = kebab_box.find(name='img').get('src')
            single_item_data.update({"img": 'http://' + img[2:]})

            # price
            price = kebab_box.find(name='span', attrs='product-price-data').text.strip()
            single_item_data.update({"new_price": price})

            # ingredients and weight
            ingredients_weight_raw = kebab_box.find(name='div', attrs='product__desc show-for-large user-inner')  
            ingredients_weight_clean = ingredients_weight_raw.find_all(name='p')
            ingredients = ingredients_weight_clean[0].text
            
            weight_raw = ingredients_weight_clean[2].text
            weight_clean = re.findall('[0-9]+', weight_raw)
            single_item_data.update({"weight": weight_clean[0]})
            single_item_data.update({"ingredients": ingredients})

            # link
            single_item_data.update({"link": page})

            # website_title
            single_item_data.update({"website_title": "1кг Счастья"})

            # website_link
            single_item_data.update({"website_link": URL})

            # category
            single_item_data.update({"category": "kebab"})

            # phone number
            single_item_data.update({"phone_number": phone_number})

            
            kebab_data.append(single_item_data)
        except Exception as error:
            print(f"[{FILE_NAME}] ERROR DURING PARSING - {error}")

    return kebab_data


def main():
    main_html = utils.get_html_page(URL)
    single_pages = get_single_pages_urls(main_html)

    kebab_data = get_kebab_data(single_pages)

    # utils.print_data(kebab_data)

    if not kebab_data:
            print(f"[!!][{FILE_NAME}] is broken")
    else:
        print(f"[{FILE_NAME}] was updated\tlength - {len(kebab_data)}")
        utils.save_json(kebab_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_ODIN_KG_SCHASTYA')
    FILE_NAME = os.getenv('FILE_NAME_ODIN_KG_SCHASTYA')
    main()




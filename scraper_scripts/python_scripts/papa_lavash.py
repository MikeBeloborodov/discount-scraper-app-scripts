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
    single_page_elements = soup.find_all(name="li", attrs='image-wrap')

    page_urls = []
    for element in single_page_elements:
        page_urls.append(element.a.get('href'))

    return page_urls


def get_shawarma_data(single_pages_urls: list) -> List[dict]:
    if not single_pages_urls:
        print(f"[{FILE_NAME}] ERROR LOADING SINGLE PAGES!")
        raise Exception

    shawarma_data = []
    for page in single_pages_urls:
        try:
            html_data = utils.get_html_page(page)

            soup = bs(html_data, "html.parser")
            shawarma_box = soup.find(name='div', id='content')
            phone_number = soup.find(name='a', attrs='top-phone').text.strip()

            single_item_data = {}
            
            # title
            title_raw = shawarma_box.find(name='h2', attrs='single-post-title').text.strip()
            title_clean = re.findall('Ш?ш?ав?е?у?рма', title_raw)
            if not title_clean:
                continue
            single_item_data.update({"title": title_raw})

            # img
            img = soup.find(name='div', attrs='woocommerce-product-gallery__image').a.get('href')
            single_item_data.update({"img": img})

            # price
            price = shawarma_box.find(name='span', attrs='woocommerce-Price-amount amount').text.strip()
            single_item_data.update({"new_price": price[:-4]})

            # ingredients and weight
            description = shawarma_box.find(name='div', id='tab-description')
            ingredients_weight = description.find_all(name='p')

            if len(ingredients_weight) == 2:
                ingredients = ingredients_weight[0].text.strip()
                weight = ingredients_weight[1].text.strip()

                single_item_data.update({"ingredients": ingredients})
                single_item_data.update({"weight": weight})
            else:
                ingredients = ingredients_weight[0].text.strip()
                single_item_data.update({"ingredients": ingredients})

            # link
            single_item_data.update({"link": page})

            # website_title
            single_item_data.update({"website_title": "Папа лаваш"})

            # website_link
            single_item_data.update({"website_link": URL})

            # category
            single_item_data.update({"category": "shawarma"})

            # phone number
            single_item_data.update({"phone_number": phone_number})

            
            shawarma_data.append(single_item_data)
        except Exception as error:
            print(f"[{FILE_NAME}] ERROR DURING PARSING - {error}")

    return shawarma_data


def main():
    main_html = utils.get_html_page(URL)
    single_pages = get_single_pages_urls(main_html)

    shawarma_data = get_shawarma_data(single_pages)

    # utils.print_data(shawarma_data)

    if not shawarma_data:
            print(f"[!!][{FILE_NAME}] is broken")
    else:
        print(f"[{FILE_NAME}] was updated\tlength - {len(shawarma_data)}")
        utils.save_json(shawarma_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_PAPA_LAVASH')
    FILE_NAME = os.getenv('FILE_NAME_PAPA_LAVASH')
    main()

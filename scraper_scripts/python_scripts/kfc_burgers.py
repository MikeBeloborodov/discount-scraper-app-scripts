from dotenv import load_dotenv
from typing import List
from scraper_scripts import utils
import os
import json
import re


def parse_api_json() -> List[dict]:
    raw_json = utils.get_json_data(URL)

    # there are layers of dictionaries
    # and we need main category to get IDs of burgers
    value = raw_json.get('value')
    categories = value.get('categories')
    main_category = categories.get('main')

    for data in main_category:
        if data['title'] == 'Бургеры':
            burger_ids = data['products']

    products = value.get('products')
    
    burger_data_raw = []
    for burger in burger_ids:
        burger_data_raw.append(products[str(burger)])

    burger_data_clean = []
    for item in burger_data_raw:
        data = {}

        # title
        title = item['title']
        data.update({'title': title})
    
        # img
        img = URL_IMG_API + item['image']
        data.update({'img': img})

        # website_title
        data.update({'website_title': 'KFC'})

        # website_link
        data.update({"website_link": URL_CLEAN})

        # link
        link = URL_PRODUCT + item['siteId']
        data.update({'link': link})

        # price
        price = str(item['price'])[:-2]
        data.update({'new_price': price})

        # ingredients
        ingredients = item['descr']
        data.update({'ingredients': ingredients})

        # category
        data.update({'category': 'burger'})

        # weight
        volume = item.get('volume')
        if volume:
            weight_raw = volume.get('gr')
            weight_clean = re.findall(r'\d+', str(weight_raw))
            data.update({'weight': weight_clean[0]})

        # phone_number
        data.update({'phone_number': '+73412908211'})

        
        burger_data_clean.append(data)

    return burger_data_clean


def main():
    try:
        # get data from website api
        burger_data = parse_api_json()
    
        # utils.print_data(burger_data)

        utils.save_json(burger_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")

if __name__=="__main__":
    load_dotenv()
    URL = os.getenv('URL_KFC_BURGERS')
    URL_PRODUCT = os.getenv('URL_KFC_BURGERS_PRODUCT_URL')
    URL_IMG_API = os.getenv('URL_KFC_BURGERS_IMG_API')
    URL_CLEAN = os.getenv('URL_KFC_BURGERS_CLEAN')
    FILE_NAME = os.getenv('FILE_NAME_KFC_BURGERS')
    main()

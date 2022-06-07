from bs4 import BeautifulSoup as bs
from typing import List
import os
from dotenv import load_dotenv
import re
import scraper_scripts.utils as utils


def get_data(html_data: str) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    pizza_box = soup.find_all(name='section', id='pizzas')
    pizza_elements = pizza_box[0].find_all(name='article')

    pizza_data = []

    for element in pizza_elements:
        data = {}
        try:
            
            # title
            if element.find(name='h3', attrs="card-title"):
                title = element.find(name='h3', attrs="card-title").text
                data.update({"title": title})
            else:
                title = element.find(name='div').text
                data.update({"title": title})

            # price
            if element.find(name='div', attrs='product-control-price'):
                price_raw = element.find(name='div', attrs='product-control-price').text
                price_clean = re.findall('[0-9]*', price_raw)[3]
                data.update({"new_price": price_clean})
            else:
                price_raw = element.find(name='button').text
                price_clean = re.findall('[0-9]*', price_raw)[0]
                data.update({"new_price": price_clean})

            # img
            img_raw = element.find(name='source').get('srcset')
            img_clean = re.findall('292w,https:\/\/dodopizza-a\.akamaihd\.net\/static\/Img\/Products\/.*366\.?p?n?g?j?p?e?g', img_raw)
            data.update({"img": img_clean[0][5:]})
            
            # link
            data.update({"link": URL})

            # phone number
            data.update({"phone_number": "8 800 302-00-60"})
            
            # website link
            data.update({'website_link': URL})
            
            # website title
            data.update({"website_title": "Додо пицца"})
            
            # category
            data.update({"category": "pizza"})
           
            # ingredients
            if element.find(name='div', attrs='card-desc'):
                ingredients = element.find(name='div', attrs='card-desc').text
                data.update({"ingredients": ingredients})
            else:
                ingredients_raw = element.find(name='main').text
                ingredients_clean = re.findall('.[А-Я].+', ingredients_raw)[0][1:]
                data.update({"ingredients": ingredients_clean})

            pizza_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return pizza_data


def main():
    try:
        if os.path.exists("./html/" + FILE_NAME + ".html"):
            with open("./html/" + FILE_NAME + ".html", "r") as file:
                html_data = file.read()
        else:
            print(f"[!!][{FILE_NAME}] html file does not exist.")
            return

        dodo_pizza_data = get_data(html_data)

        if not dodo_pizza_data:
            print(f"[!!][{FILE_NAME}] is broken")
        else:
            print(f"[{FILE_NAME}] was updated\tlength - {len(dodo_pizza_data)}")
            utils.save_json(dodo_pizza_data, FILE_NAME)
            print(f"[{FILE_NAME}] json file created")

    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    FILE_NAME = os.getenv('FILE_NAME_DODO_PIZZA')
    URL = os.getenv('URL_DODO_PIZZA')
    main()
    
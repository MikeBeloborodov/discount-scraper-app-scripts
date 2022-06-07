from bs4 import BeautifulSoup as bs
from typing import List
import os
from dotenv import load_dotenv
import re
import utils


def get_data(html_data: str) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    pizza_box = soup.find_all(name='div', id='pizza-box')
    pizza_elements = pizza_box[0].find_all(name='div', attrs='goods -resize')
    phone_number = soup.find(name='a', attrs="mode-phone").text

    pizza_data = []

    for element in pizza_elements:
        data = {}
        try:
           
            # title
            title = element.find(name='div', attrs='goods-name item-name').text.strip()
            data.update({"title": title})
            
            # price
            price = element.find(name='div', attrs='price').text.strip()[:-3]
            data.update({'new_price': price})
            
            # img
            img = element.find(name='img', attrs='item-image').get('src')
            data.update({'img': URL[:-1] + img})
            
            # link
            data.update({"link": URL})

            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({'website_link': URL})
           
            # website title
            data.update({"website_title": "Мама пицца"})
            
            # category
            data.update({"category": "pizza"})

            # ingredients
            ingredients_raw = element.find(name='div', attrs='goods-meta').text.strip()
            ingredients_clean = re.findall('.*', ingredients_raw)[0]
            data.update({'ingredients': ingredients_clean})

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

        mama_pizza_data = get_data(html_data)
        if not mama_pizza_data:
            print(f"[!!][{FILE_NAME}] is broken")
        else:
            print(f"[{FILE_NAME}] was updated\tlength - {len(mama_pizza_data)}")
            utils.save_json(mama_pizza_data, FILE_NAME)
            print(f"[{FILE_NAME}] json file created")
    
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    FILE_NAME = os.getenv('FILE_NAME_MAMA_PIZZA')
    URL = os.getenv('URL_MAMA_PIZZA')
    main()
    
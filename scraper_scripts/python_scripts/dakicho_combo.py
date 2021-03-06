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
    combo_element_boxes = soup.find_all(name='div', attrs='js-product')
    phone_number = soup.find(name='div', attrs='t-text').a.text

    combo_data = []

    for element in combo_element_boxes:
        data = {}
        try:

            # title
            title_raw = element.find(name='div', attrs='js-store-prod-name').text
            if not title_raw:
                continue
            
            title_clean = re.findall('(К?к?омбо)', title_raw)
            if not title_clean:
                continue
            
            data.update({"title": title_raw})
            
            # price
            price = element.find(name='div', attrs='js-product-price').text
            data.update({"new_price": price})

            # img
            img = element.find(name='img').get('src')
            data.update({"img": img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            data.update({"phone_number": phone_number})
            
            # website link
            data.update({'website_link': URL})
            
            # website title
            data.update({"website_title": "Дак и чо"})
            
            # category
            data.update({"category": "combo"})
            
            # ingredients
            ingredients_raw = str(element.find(name='div', attrs='js-store-prod-descr')).replace('<br/>', ' ')
            ingredients_clean = re.findall('\d\..+\.?<', ingredients_raw)[0][:-1]
            
            data.update({"ingredients": ingredients_clean})

            combo_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return combo_data


def main():
    try:
        if os.path.exists("./html/" + HTML_FILE_NAME + ".html"):
            with open("./html/" + HTML_FILE_NAME + ".html", "r") as file:
                html_data = file.read()
        else:
            print(f"[!!][{FILE_NAME}] html file does not exist.")
            return

        dakicho_combo_data = get_data(html_data)

        if not dakicho_combo_data:
            print(f"[!!][{FILE_NAME}] is broken")
        else:
            print(f"[{FILE_NAME}] was updated\tlength - {len(dakicho_combo_data)}")
            utils.save_json(dakicho_combo_data, FILE_NAME)
            print(f"[{FILE_NAME}] json file created")

        
    except Exception as error:
        print(f"[{FILE_NAME}] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    FILE_NAME = os.getenv('FILE_NAME_DAKICHO_COMBO')
    HTML_FILE_NAME=os.getenv('FILE_NAME_DAKICHO')
    URL = os.getenv('URL_DAKICHO')
    main()
    
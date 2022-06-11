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
    hinkali_box = soup.find(name='div', attrs='t778__container t-container t778__container_mobile-flex')
    elements = hinkali_box.find_all(name='div', attrs='t778__wrapper')
    phone_number = soup.find_all(name='div', attrs='t491__title t-name t-name_sm')[2].text.strip()

    dumplings_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='div', attrs='t778__title').text.strip()
            if re.match('соус', title, re.I):
                continue
            data.update({"title": title})
            
            # prices
            price = element.find(name='div', attrs='t778__price-value').text.strip()
            price_clean = re.findall(r'\d+', price)
            data.update({"new_price": price_clean[0]})

            # img
            img = element.find(name='div', attrs='t778__bgimg').get('data-original').strip()
            data.update({"img": img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            phone_number_clean = re.findall(r'\+.+', phone_number)[0]
            data.update({"phone_number": phone_number_clean})
            
            # website link
            data.update({"website_link": URL})
            
            # website title
            data.update({"website_title": "Парус 18"})
            
            # category
            data.update({"category": "dumplings"})

            # ingredients
            ingredients = str(element.find(name='div', attrs='t778__descr t-descr t-descr_xxs'))
            ingredients_clean = re.findall('\s?[А-я][А-я, 0-9c]+', ingredients)
            new_ingredients_string = ''
            for part in ingredients_clean:
                if not part:
                    continue
                new_ingredients_string += part + " "
            data.update({"ingredients": new_ingredients_string.replace('  ', ' ')})

            dumplings_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return dumplings_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        parus18_data = get_data(html_data)

        # utils.print_data(parus18_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(parus18_data)}")
        utils.save_json(parus18_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")

    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_PARUS18')
    FILE_NAME = os.getenv('FILE_NAME_PARUS18')
    main()

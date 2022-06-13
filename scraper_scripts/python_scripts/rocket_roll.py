from bs4 import BeautifulSoup as bs
from typing import List
import scraper_scripts.utils as utils
import os
from dotenv import load_dotenv
import json
import re


def get_data(html_data: bytes) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='script', type='application/ld+json')
    phone_number = soup.find(name='div', attrs='tel').text

    sushi_set_data = []

    for element in elements:
        json_format = json.loads(element.text)
        offer_data = json_format['offers']
        data = {}
        try:
            # title
            title = json_format["name"]
            data.update({"title": title})

            # new price
            new_price = offer_data["lowPrice"]
            data.update({"new_price": new_price})

            # old price
            old_price = offer_data["highPrice"]
            data.update({"old_price": old_price})

            # img
            img = json_format['image']
            data.update({"img": img[0]})

            # website link
            data.update({"website_link": URL_NORMAL})

            # website title
            data.update({"website_title": "RocketRoll"})

            # link
            data.update({"link": URL})

            # category
            data.update({"category": "sushi"})

            # ingredients
            ingredients = json_format['description']
            data.update({"ingredients": ingredients})

            # phone number
            data.update({"phone_number": phone_number})

            sushi_set_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")
    
    # weight
    weight_elements = soup.find_all('script', {"data-content": "rollpreorder"})
    for counter, data in enumerate(weight_elements):
        if data:
            weight_raw = data.text
            weight_clean = re.findall(r'\d+\sгр', weight_raw)
            sushi_set_data[counter].update({"weight": weight_clean[0][:-3]})

    return sushi_set_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        sushi_rocket_roll_data = get_data(html_data)

        # utils.print_data(sushi_rocket_roll_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(sushi_rocket_roll_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(sushi_rocket_roll_data)}")
        utils.save_json(sushi_rocket_roll_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_ROCKET_ROLL')
    URL_NORMAL = os.getenv('URL_ROCKET_ROLL_NORMAL')
    FILE_NAME = os.getenv('FILE_NAME_ROCKET_ROLL')
    main()

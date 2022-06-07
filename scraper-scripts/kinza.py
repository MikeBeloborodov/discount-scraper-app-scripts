from typing import List
import utils
import os
from dotenv import load_dotenv
import re


def get_data(json_data) -> List[dict]:
    dumplings_data = []

    try:
        for element in json_data['products']:
            
            data = {}

            # title
            title_raw = element['title']
            title_clean = re.findall('[А-я\s]+\s', title_raw)[0][:-1]
            data.update({"title": title_clean})

            # price
            price = element['price'][:-5]
            data.update({"new_price": price})
            
            # img
            img = element['gallery'][9:-3].replace("\\", "")
            data.update({"img": img})

            # link
            data.update({"link": URL_NORMAL})

            # phone number
            data.update({"phone_number": '+7 3412 77-22-52'})

            # website link
            data.update({'website_link': URL_NORMAL})
           
            # website title
            data.update({"website_title": "Кинза"})

            # category
            data.update({"category": "dumplings"})

            # ingredients
            ingredients = element['descr'].strip().replace('<br />' , ' ').replace('&nbsp;', ' ')
            data.update({"ingredients": ingredients})

            # weight
            weight_raw = element['title'].strip()
            weight_clean = re.findall('[0-9].*', weight_raw)[0]
            data.update({"weight": weight_clean})
            
            dumplings_data.append(data)

    except Exception as error:
        print(f"Error in {FILE_NAME} - {error}")

    return dumplings_data


def main():
    try:
        json_data = utils.get_json_data(URL)
        dumplings_data = get_data(json_data)
        
        utils.save_json(dumplings_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_KINZA')
    URL_NORMAL = os.getenv('URL_KINZA_NORMAL')
    FILE_NAME = os.getenv('FILE_NAME_KINZA')
    main()

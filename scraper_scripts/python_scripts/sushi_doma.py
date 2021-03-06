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
    elements = soup.find_all(name='div', attrs='product-card')
    phone_number = soup.find(name='div', attrs="profile-content").a.get('href')[4:]

    sushi_set_data = []

    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='div', attrs='card-title').text.strip()
            data.update({"title": title})
            
            # price
            prices = element.find_all(name='span', attrs="price-value")
            if len(prices) == 2:
                data.update({"old_price": f"{prices[1].text[:-2]}".replace(' ', '')})
                data.update({"new_price": f"{prices[0].text[:-2]}".replace(' ', '')})
            else:
                data.update({"new_price": f"{prices[0].text[:-2]}".replace(' ', '')})
            
            # img
            img_raw = element.find(name='div', attrs='v-lazy-img cursor-pointer lazy-load flex').get('style')
            img_clean = re.findall('http.*"', str(img_raw))
            data.update({"img": img_clean[0][:-1]})
            
            # link
            data.update({"link": URL})
            
            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({'website_link': URL})

            # website title
            data.update({"website_title": "Суши дома"})

            # ingredients
            ingredients = element.find(name='div', attrs='card-description').text.strip().replace('\n', ' ')
            data.update({"ingredients": ingredients})

            # category
            data.update({"category": "sushi"})

            sushi_set_data.append(data)
        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return sushi_set_data


def main():
    try:
        if os.path.exists("./html/" + FILE_NAME + ".html"):
            with open("./html/" + FILE_NAME + ".html", "r") as file:
                html_data = file.read()
        else:
            print(f"[!!][{FILE_NAME}] html file does not exist.")
            return

        sushi_doma_data = get_data(html_data)
        
        # utils.print_data(sushi_doma_data)
        
        if not sushi_doma_data:
            print(f"[!!][{FILE_NAME}] is broken")
        else:
            print(f"[{FILE_NAME}] was updated\tlength - {len(sushi_doma_data)}")
            utils.save_json(sushi_doma_data, FILE_NAME)
            print(f"[{FILE_NAME}] json file created")
            
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    FILE_NAME = os.getenv('FILE_NAME_SUSHI_DOMA')
    URL = os.getenv('URL_SUSHI_DOMA')
    main()

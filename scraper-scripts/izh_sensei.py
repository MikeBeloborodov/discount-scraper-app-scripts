from bs4 import BeautifulSoup as bs
from typing import List
import utils
import os
from dotenv import load_dotenv
import re


def get_data(html_data: str, url: str) -> List[str]:
    if not html_data:
        return None
        
    soup = bs(html_data, "html.parser")
    elements = soup.find_all('div', attrs='catalog__item')
    phone_number = soup.find('ul', 'footer__list').a.get('href')

    sushi_set_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='div', attrs="catalog__prod-title").text
            data.update({"title": title})
            
            # weight
            if element.find('div', attrs="catalog__item-weight"):
                weight = element.find('div', attrs="catalog__item-weight").text.strip()
            else:
                weight_raw = element.find('div', attrs="catalog__descr").text.strip()
                weight_cleaned = re.findall('[0-9,]+\s?к?гр?', weight_raw)
                if not weight_cleaned:
                    weight = weight_cleaned
                else:
                    weight = weight_cleaned[0]
            data.update({"weight": weight})
            
            # prices
            prices_raw = element.find(name='div', attrs='catalog__by-group').text.strip().replace(" ", "")
            prices_clean = re.findall('[0-9]+', prices_raw)
            if len(prices_clean) == 2:
                data.update({"old_price": f"{str(prices_clean[0])} руб"})
                data.update({"new_price": f"{str(prices_clean[1])} руб"})
            else:
                data.update({"new_price": f"{str(prices_clean[0])} руб"})
            
            # img
            data.update({"img": os.getenv('URL_IZH_SENSEI_CLEAN') + element.img.get('src')[2:]})
            
            # link
            data.update({"link": url})
            
            # phone number
            data.update({"phone_number": phone_number[4:]})
            
            # website link
            data.update({"website_link": os.getenv('URL_IZH_SENSEI_CLEAN')})

            # website title
            data.update({"website_title" : "Izh sensei"})

            # cathegory
            data.update({"cathegory": "sushi"})

            sushi_set_data.append(data)

        except Exception as error:
            print(error)

    return sushi_set_data

def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_IZH_SENSEI')
        FILE_NAME = os.getenv('FILE_NAME_IZH_SENSEI')

        html_data = utils.get_html_page(URL)
        izh_sensei_data = get_data(html_data, URL)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(izh_sensei_data)}")
        utils.save_json(izh_sensei_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occured: {error}")

if __name__ == "__main__":
    main()
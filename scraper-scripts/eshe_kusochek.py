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
    elements = soup.find_all(name='div', attrs='prod_item item_t_1')
    phone_number = soup.find(name='div', attrs='tel').text

    sushi_set_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='div', attrs="pitem_name").text
            data.update({"title": title})
            
            # weight
            weight = element.find(name='div', attrs="pitem_weight").text
            data.update({"weight": weight})
           
            # prices
            price = element.find(name='div', attrs='pitem_price').text[:-2]
            data.update({"new_price": price})
            
            # img
            img_raw = element.find(name='div', attrs='pitem_img').get('style')
            img_clean = re.findall('img.*\'', img_raw)[0][:-1]
            data.update({'img': url[:19] + img_clean})
            
            # link
            data.update({"link": url})
            
            # phone number
            data.update({"phone_number": phone_number})
            
            # website link
            data.update({"website_link": url})
            
            # website title
            data.update({"website_title": "Ещё кусочек"})
            
            # cathegory
            data.update({"cathegory": "pizza"})

            #ingredients
            ingredients = element.find(name='div', attrs='pitem_descr').text
            data.update({"ingredients": ingredients})

            sushi_set_data.append(data)
        except Exception as error:
            print(error)

    return sushi_set_data[:-1]

def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_ESHE_KUSOCHEK')
        FILE_NAME = os.getenv('FILE_NAME_ESHE_KUSOCHEK')

        html_data = utils.get_html_page(URL)
        eshe_kusochek_data = get_data(html_data, URL)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(eshe_kusochek_data)}")
        utils.save_json(eshe_kusochek_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")

    except Exception as error:
        print(f"[!!!] An error occured: {error}")


if __name__ == "__main__":
    main()
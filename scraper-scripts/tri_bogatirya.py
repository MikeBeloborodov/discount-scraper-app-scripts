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
    elements = soup.find_all(name='div', attrs='menu-item')
    phone_number = soup.find(name='span', attrs='tel-inner').text.strip()

    kebab_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='a', attrs='modalbox').text.strip()
            data.update({"title": title})

            # prices
            price = element.find_all(name='p')[1].text.strip()[6:-5]
            data.update({"new_price": price})

            # img
            img = element.find(name='img').get('src')
            data.update({"img": url[:-6] + img})
            
            # link
            data.update({"link": url})
            
            # phone number
            data.update({"phone_number": phone_number[6:]})
           
            # website link
            data.update({"website_link": url})
            
            # website title
            data.update({"website_title": "Три богатыря"})

            # ingredients
            ingredients = element.find_all(name='p')[0].text.strip()
            data.update({"ingredients": ingredients})
            
            # cathegory
            data.update({"cathegory": "kebab"})

            kebab_data.append(data)

        except Exception as error:
            print(error)

    return kebab_data[:-3]

def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_TRI_BOGATIRYA')
        FILE_NAME = os.getenv('FILE_NAME_TRI_BOGATIRYA')

        html_data = utils.get_html_page(URL)
        tri_bogatirya_data = get_data(html_data, URL)
        
        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(tri_bogatirya_data)}")
        utils.save_json(tri_bogatirya_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occured: {error}")


if __name__ == "__main__":
    main()
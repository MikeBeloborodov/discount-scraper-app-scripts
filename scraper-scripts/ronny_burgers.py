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
    burger_box = soup.find('ul', {"rel-code": "burges"})
    elements = burger_box.find_all(name='div', attrs='meal-item separator')
    phone_number = soup.find(name='p', attrs='delivery-phone').text.strip()

    burger_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='p', attrs='meal-name').text.strip()
            data.update({"title": title})
            
            # prices
            price = element.find(name='p', attrs='meal-price').text.strip()
            data.update({"new_price": price[:-3]})
            
            # img
            img = element.find(name='img').get('src').replace(' ', '%20')
            data.update({"img": url[:-7] + img})
           
            # link
            data.update({"link": url})
            
            # phone number
            data.update({"phone_number": phone_number})
            
            # website link
            data.update({"website_link": url})
            
            # website title
            data.update({"website_title": "Ронни"})
            
            # cathegory
            data.update({"cathegory": "burger"})
            burger_data.append(data)
       
        except Exception as error:
            print(error)

    return burger_data

def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_RONNY_BURGERS')
        FILE_NAME = os.getenv('FILE_NAME_RONNY_BURGERS')

        html_data = utils.get_html_page(URL)
        ronny_burgers_data = get_data(html_data, URL)
        
        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(ronny_burgers_data)}")
        utils.save_json(ronny_burgers_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")

    except Exception as error:
        print(f"[!!!] An error occured: {error}")


if __name__ == "__main__":
    main()
from bs4 import BeautifulSoup as bs
from typing import List
import utils
import os
from dotenv import load_dotenv


def get_data(html_data: str, url: str) -> List[str]:
    if not html_data:
        return None
        
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='page-list-ext-item')
    phone_number = soup.find(id="phone").a.string

    sushi_set_data = []

    for element in elements:
        data = {}
        try:
            # title
            data.update({"title": element.h3.a.get('title')})
            
            # weight
            weight_and_price = element.find_all(name='b')
            data.update({"weight": f"{weight_and_price[0].string} гр"})
            
            # price
            data.update({"new_price": f"{weight_and_price[1].string} руб"})
            
            # img
            data.update({"img": element.img.get('src')})
            
            # link
            data.update({"link": element.a.get('href')})
            
            # phone number
            data.update({"phone_number": phone_number})

            # website
            data.update({"website": url})

            # cathegory
            data.update({"cathegory": "sushi"})

            sushi_set_data.append(data)
        except:
            pass
    return sushi_set_data


def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_IMPERIO')
        FILE_NAME = os.getenv('FILE_NAME_IMPERIO')

        html_data = utils.get_html_page(URL)
        sushi_imperio_data = get_data(html_data, URL)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(sushi_imperio_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(sushi_imperio_data)}")
        utils.save_json(sushi_imperio_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occured: {error}")

if __name__ == "__main__":
    main()
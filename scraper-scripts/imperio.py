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

            sushi_set_data.append(data)
        except:
            pass
    return sushi_set_data


def main():
    try:
        load_dotenv()

        URL = os.getenv('URL_IMPERIO')
        FILE_NAME = os.getenv('FILE_NAME_IMPERIO')
        html_data_new = ""
        html_data_old = ""

        html_data_new = utils.get_html_page(URL)

        if os.path.exists("./html/" + FILE_NAME + ".html"):
            with open("./html/" + FILE_NAME + ".html", "r") as file:
                html_data_old = file.read()

        sushi_imperio_new_data = get_data(html_data_new, URL)
        sushi_imperio_old_data = get_data(html_data_old, URL)

        if sushi_imperio_new_data == sushi_imperio_old_data:
            print(f"[{FILE_NAME}] is up to date\tlength - {len(sushi_imperio_new_data)}")
        else:
            with open("./html/" + FILE_NAME + ".html", "w") as file:
                file.write(str(html_data_new))
            print(f"[!!][{FILE_NAME}] was updated\tlength - {len(sushi_imperio_new_data)}")
            # send data to api
    except Exception as error:
        print(f"[!!!] An error occured: {error}")

if __name__ == "__main__":
    main()
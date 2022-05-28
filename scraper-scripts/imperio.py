from bs4 import BeautifulSoup as bs
from typing import List
import utils
import os
from dotenv import load_dotenv


def get_data(html_data: str) -> List[str]:
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='page-list-ext-item')
    phone_number = soup.find(id="phone").a.string

    sushi_set_data = []

    for element in elements:
        data = {}
        try:
            data.update({"title": element.h3.a.get('title')})
            weight_and_price = element.find_all(name='b')
            data.update({"weight": f"{weight_and_price[0].string} гр"})
            data.update({"price": f"{weight_and_price[1].string} руб"})
            data.update({"img": element.img.get('src')})
            data.update({"link": element.a.get('href')})
            data.update({"phone_number": phone_number})
            sushi_set_data.append(data)
        except:
            pass
    return sushi_set_data


load_dotenv()

URL = os.getenv('URL_IMPERIO')
FILE_NAME = os.getenv('FILE_NAME_IMPERIO')
html_data_new = ""
html_data_old = ""

html_data_new = utils.get_html_page(URL, FILE_NAME)

with open(FILE_NAME + ".html", "r") as file:
    html_data_old = file.read()

sushi_imperio_new_data = get_data(html_data_new)
sushi_imperio_old_data = get_data(html_data_old)

if sushi_imperio_new_data == sushi_imperio_old_data:
    print("Up to date")
else:
    with open(FILE_NAME + ".html", "w") as file:
        file.write(html_data_new)
    print(sushi_imperio_new_data)
    # send data to api
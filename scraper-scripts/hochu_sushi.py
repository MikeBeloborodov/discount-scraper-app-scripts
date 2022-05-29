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
    elements = soup.find_all('div', {"class": re.compile('product_item cleared')})
    phone_number = soup.find('a', 'tel2 ya-phone').get('href')

    sushi_set_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='div', attrs="name").text
            data.update({"title": title})
            
            # weight
            weight = element.find('div', attrs="weight").text
            data.update({"weight": weight})
            
            # prices
            prices_raw = element.find('div', attrs="price").text
            prices_clean = re.findall('[0-9\s]*\s?р', str(prices_raw))
            if len(prices_clean) == 2:
                data.update({"old_price": f"{str(prices_clean[0][:-2])} руб"})
                data.update({"new_price": f"{str(prices_clean[1][:-2])} руб"})
            else:
                data.update({"new_price": f"{str(prices_clean[0][:-2])} руб"})

            
            # img
            data.update({"img": element.img.get('src')})
            
            # link
            data.update({"link": url})
            
            # phone number
            data.update({"phone_number": phone_number[3:]})
            
            # website
            data.update({"website": url})
            
            sushi_set_data.append(data)
        except Exception as error:
            print(error)

    return sushi_set_data

def main():
    load_dotenv()

    URL = os.getenv('URL_HOCHU_SUSHI')
    FILE_NAME = os.getenv('FILE_NAME_HOCHU_SUSHI')
    html_data_new = ""
    html_data_old = ""

    html_data_new = utils.get_html_page(URL, FILE_NAME)

    if os.path.exists("./html/" + FILE_NAME + ".html"):
        with open("./html/" + FILE_NAME + ".html", "r") as file:
            html_data_old = file.read()

    hochu_sushi_new_data = get_data(html_data_new, URL)
    hochu_sushi_old_data = get_data(html_data_old, URL)

    if hochu_sushi_new_data == hochu_sushi_old_data:
        print(f"[{FILE_NAME}] is up to date\tlength - {len(hochu_sushi_new_data)}")
    else:
        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(html_data_new)
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(hochu_sushi_new_data)}")
        # send data to api

if __name__ == "__main__":
    main()
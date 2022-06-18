from bs4 import BeautifulSoup as bs
from typing import List
import scraper_scripts.utils as utils
import os
from dotenv import load_dotenv
import re


def get_data(html_data: bytes) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    elements = soup.find_all(name='div', attrs='product-thumb')
    # phone number
    info_elements = soup.find_all(name='div', attrs='center-info-title')
    for element in info_elements:
        if element.a:
            phone_number_raw = element.a.text.strip()
            phone_number_clean = re.findall('3412', phone_number_raw)
            if phone_number_clean:
                phone_number = phone_number_raw

    shawarma_data = []

    for element in elements:
        data = {}
        try:

            # title
            title = element.find(name='a', attrs='product-title').text.strip()
            data.update({"title": title})
            
            # weight
            weight = element.find(name='div', attrs='food__feature').text.strip()
            data.update({"weight": weight[:-2]})
            
            # price
            price = element.find(name='div', attrs='food__price').text.strip()
            data.update({"new_price": price[:-2]})
            
            # img
            img = element.find(name='img').get('data-src')
            data.update({"img": img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({"website_link": URL_CLEAN})

            # website title
            data.update({"website_title": "Panda Grill"})

            # ingredients
            ingredients = element.find('p', {"itemprop": "description"}).text.strip()
            data.update({"ingredients": ingredients})

            # category
            data.update({"category": "shawarma"})

            shawarma_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return shawarma_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        pandagrill_data = get_data(html_data)

        # utils.print_data(pandagrill_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(pandagrill_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(pandagrill_data)}")
        utils.save_json(pandagrill_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_PANDAGRILL')
    URL_CLEAN = os.getenv('URL_PANDAGRILL_CLEAN')
    FILE_NAME = os.getenv('FILE_NAME_PANDAGRILL')
    main()



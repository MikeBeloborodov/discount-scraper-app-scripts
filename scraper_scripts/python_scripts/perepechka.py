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
    
    elements = soup.find_all(name='div', attrs='s6_box-2')
    phone_number = soup.find(name='a', attrs='tel _1 w-button').get('href')

    pie_data = []
    for element in elements:
        data = {}
        try:
            # title
            title = element.find(name='a', attrs='h3_link').text.strip()
            if title == "Подарок":
                continue
            data.update({"title": title})

            # prices
            price = element.find(name='div', attrs='price-2').text.strip()[:-7]
            data.update({"new_price": price})

            # img
            img_raw = element.find(name='div', attrs='product_bg-3').get('style')
            img_clean = re.findall('h.+g', img_raw)[0]
            data.update({"img": img_clean})
            
            # link
            link = element.find(name='a', attrs='tel _1 w-button').get('href')
            data.update({"link": link})
            
            # phone number
            data.update({"phone_number": phone_number[4:]})
            
            # website link
            data.update({"website_link": URL})
            
            # website title
            data.update({"website_title": "Перепечка"})
            
            # category
            data.update({"category": "pie"})

            pie_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return pie_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        perepechka_data = get_data(html_data)
        
        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(perepechka_data)}")
        utils.save_json(perepechka_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_PEREPECHKA')
    FILE_NAME = os.getenv('FILE_NAME_PEREPECHKA')
    main()

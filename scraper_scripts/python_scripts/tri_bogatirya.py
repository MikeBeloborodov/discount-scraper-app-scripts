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
    elements = soup.find_all(name='div', attrs='menu-item')
    phone_number = soup.find(name='span', attrs='tel-inner').text.strip()

    kebab_data = []
    for element in elements:
        data = {}
        try:
            # title
            title_raw = element.find(name='a', attrs='modalbox').text.strip()
            bad_title = re.findall('К?к?артошка', title_raw)
            if bad_title:
                continue
            data.update({"title": title_raw})

            # prices
            price = element.find_all(name='p')[1].text.strip()[6:-5]
            data.update({"new_price": price})

            # img
            img = element.find(name='img').get('src')
            data.update({"img": URL[:-6] + img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            data.update({"phone_number": phone_number[6:]})
           
            # website link
            data.update({"website_link": URL})
            
            # website title
            data.update({"website_title": "Три богатыря"})

            # ingredients
            ingredients = element.find_all(name='p')[0].text.strip()
            if ingredients == 'ПорцияСоус':
                continue
            data.update({"ingredients": ingredients})
            
            # category
            data.update({"category": "kebab"})

            kebab_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return kebab_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        tri_bogatirya_data = get_data(html_data)
        
        # utils.print_data(tri_bogatirya_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(tri_bogatirya_data)}")
        utils.save_json(tri_bogatirya_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_TRI_BOGATIRYA')
    FILE_NAME = os.getenv('FILE_NAME_TRI_BOGATIRYA')
    main()

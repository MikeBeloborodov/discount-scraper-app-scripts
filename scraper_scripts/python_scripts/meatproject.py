from bs4 import BeautifulSoup as bs
from typing import List
import os
from dotenv import load_dotenv
import re
import scraper_scripts.utils as utils


def get_data(html_data: str) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    kebab_elements = soup.find_all(name='div', attrs='js-product')
    phone_number_elements = soup.find_all(name='a', attrs='tn-atom')
    for element in phone_number_elements:
        href_raw = element.get('href')
        href_clean = re.findall('tel', href_raw)
        if href_clean:
            phone_number = href_raw

    kebab_data = []

    for element in kebab_elements:
        data = {}
        try:
           
            # title
            title_raw = element.find(name='div', attrs='js-store-prod-name').text.strip()
            title_combo = re.findall('С?с?ет', title_raw)
            title_kebab = re.findall('Ш?ш?ашлык', title_raw)
            title_shawarma = re.findall('Ш?ш?аверма', title_raw)
            title_marinade = re.findall('М?маринованный', title_raw)
            # names we need
            if not title_combo and not title_kebab:
                continue
            # names we don't need
            if title_shawarma or title_marinade:
                continue
            data.update({"title": title_raw})
            
            # price new
            price_new = element.find(name='div', attrs='js-product-price').text.strip().replace(" ", "")
            data.update({"new_price": price_new})

            # price old
            if element.find(name='div', attrs='js-store-prod-price-old-val'):
                price_old = element.find(name='div', attrs='js-store-prod-price-old-val').text.strip()
                if price_old:
                    data.update({"old_price": price_old.replace(" ", "")})
            
            # img
            img = element.find(name='div', attrs='js-product-img').get('data-original')
            data.update({"img": img})
            
            # link
            link = element.a.get('href')
            data.update({"link": link})

            # phone number
            data.update({"phone_number": phone_number})

            # website link
            data.update({"website_link": URL})
           
            # website title
            data.update({"website_title": "MeatProject"})
            
            # category
            data.update({"category": 'kebab'})

            # ingredients
            ingredients = element.find(name='div', attrs='js-store-prod-descr').text.strip()
            data.update({"ingredients": ingredients})

            kebab_data.append(data)

        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return kebab_data


def main():
    try:
        if os.path.exists("./html/" + FILE_NAME + ".html"):
            with open("./html/" + FILE_NAME + ".html", "r") as file:
                html_data = file.read()
        else:
            print(f"[!!][{FILE_NAME}] html file does not exist.")
            return

        meatproject_data = get_data(html_data)
        # utils.print_data(meatproject_data)

        if not meatproject_data:
            print(f"[!!][{FILE_NAME}] is broken")
        else:
            print(f"[{FILE_NAME}] was updated\tlength - {len(meatproject_data)}")
            utils.save_json(meatproject_data, FILE_NAME)
            print(f"[{FILE_NAME}] json file created")
    
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    FILE_NAME = os.getenv('FILE_NAME_MEATPROJECT')
    URL = os.getenv('URL_MEATPROJECT')
    main()
    


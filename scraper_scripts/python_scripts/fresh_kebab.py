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
    elements = soup.find_all(name='div', attrs='t776__content')
    phone_number_div = soup.find('div', 't396')
    phone_number_elements = phone_number_div.find_all(name='div', attrs='tn-atom')
    for element in phone_number_elements:
        phone_number_raw = element.text
        phone_number_clean = re.findall('Телефон', phone_number_raw)
        if not phone_number_clean:
            continue
        phone_number = phone_number_raw

    kebab_data = []
    for element in elements:
        data = {}
        try:
            # title
            title_raw = element.find('div', attrs='t776__title').text.strip()
            title_clean = re.findall('Ш?ш?аурма', title_raw)
            if not title_clean:
                continue
            data.update({"title": title_raw})
            
            # prices
            price = element.find('div', attrs='t776__price-value').text.strip()
            data.update({"new_price": price})
            
            # img
            img = element.find('img').get('data-original')
            data.update({"img": img})
            
            # link
            data.update({"link": URL})
            
            # phone number
            phone_number_no_text = re.findall('\d+-\d+', phone_number)
            data.update({"phone_number": phone_number_no_text[0]})
            
            # website link
            data.update({"website_link": URL})

            # website title
            data.update({"website_title": "FreshKebab"})

            # ingredients
            ingredients = element.find('div', attrs='t776__descr').text
            data.update({"ingredients": ingredients})

            # category
            data.update({"category": "shawarma"})

            kebab_data.append(data)
        except Exception as error:
            print(f"Error in {FILE_NAME} - {error}")

    return kebab_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        fresh_kebab_data = get_data(html_data)

        # utils.print_data(fresh_kebab_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))

        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(fresh_kebab_data)}")
        utils.save_json(fresh_kebab_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_FRESH_KEBAB')
    FILE_NAME = os.getenv('FILE_NAME_FRESH_KEBAB')
    main()


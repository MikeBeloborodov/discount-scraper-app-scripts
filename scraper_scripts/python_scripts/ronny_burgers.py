from bs4 import BeautifulSoup as bs
from typing import List
import scraper_scripts.utils as utils
import os
from dotenv import load_dotenv


def get_data(html_data: bytes) -> List[dict]:
    if not html_data:
        print(f"Error while getting data - {FILE_NAME}")
        raise Exception
        
    soup = bs(html_data, "html.parser")
    burger_box = soup.find(name='div', attrs='mobile-catalog')
    elements = burger_box.find_all(name='div', attrs='meal-section-mobile flexslider clear')
    phone_number = soup.find(name='p', attrs='delivery-phone').text.strip()

    burger_data = []
    for element in elements:
        if element.find(name='h5').text != 'Бургеры':
            continue
        else:
            burger_elements = element.find_all(name='li')
            for burger in burger_elements:
                data = {}
                try:
                    # title
                    title_raw = burger.find(name='p', attrs='meal-name')
                    if not title_raw:
                        continue
                    title = burger.find(name='p', attrs='meal-name').text.strip()
                    data.update({"title": title})
                
                    # prices
                    price_raw = burger.find(name='span', attrs='meal-price')
                    if not price_raw:
                        continue
                    price = burger.find(name='span', attrs='meal-price').text.strip()
                    data.update({"new_price": price[:-3]})
                    
                    # img
                    img = burger.find(name='img').get('src').replace(' ', '%20')
                    data.update({"img": URL[:-7] + img})
                    
                    # link
                    data.update({"link": URL})
                    
                    # phone number
                    data.update({"phone_number": phone_number})
                
                    # website link
                    data.update({"website_link": URL})
                    
                    # website title
                    data.update({"website_title": "Ронни"})

                    # weight
                    weight = burger.find(name='div', attrs='meal-content-weight').text.strip()
                    data.update({"weight": weight})
                    
                    # ingredients
                    ingredients = burger.find(name='div', attrs='meal-content-text').text.strip().replace('\xa0', ' ')
                    data.update({"ingredients": ingredients})

                    # category
                    data.update({"category": "burger"})
                    
                    burger_data.append(data)

                except Exception as error:
                    print(f"Error in {FILE_NAME} - {error}")

    return burger_data


def main():
    try:
        html_data = utils.get_html_page(URL)
        ronny_burgers_data = get_data(html_data)
        
        # utils.print_data(ronny_burgers_data)

        with open("./html/" + FILE_NAME + ".html", "w") as file:
            file.write(str(html_data))
        print(f"[!!][{FILE_NAME}] was updated\tlength - {len(ronny_burgers_data)}")
        utils.save_json(ronny_burgers_data, FILE_NAME)
        print(f"[{FILE_NAME}] json file created")
        
    except Exception as error:
        print(f"[!!!] An error occurred: {error}")


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('URL_RONNY_BURGERS')
    FILE_NAME = os.getenv('FILE_NAME_RONNY_BURGERS')
    main()

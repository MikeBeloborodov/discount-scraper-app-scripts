from bs4 import BeautifulSoup as bs
import re
from typing import List
import utils
import os
from dotenv import load_dotenv


def get_names(html_data: str, 
                html_element: str, 
                html_element_attrs: str,
                pattern: str) -> List[str] | bool:
    soup = bs(html_data, "html.parser")
    names = soup.find_all(name=html_element, attrs=html_element_attrs)
    sushi_set_names_raw = re.findall(pattern, str(names))

    sushi_set_names_clean = []
    for name in sushi_set_names_raw:
        sushi_set_names_clean.append(name[1:len(name) - 3])
    
    if len(sushi_set_names_clean) == len(names):
        return sushi_set_names_clean
    else:
        return False

load_dotenv()

URL = os.getenv('URL_IMPERIO')
FILE_NAME = os.getenv('FILE_NAME_IMPERIO')
html_data = ""


if os.path.exists(FILE_NAME + ".html"):
    print("from file")
    with open(FILE_NAME + ".html", "r") as file:
        html_data = file.read()
else:
    print("from website")
    html_data = utils.get_html_page(URL, FILE_NAME)

sushi_set_names = get_names(html_data, 'h3', 'page-list-ext-title', '>[^<][А-я\s"1-9#№A-z]*<\/a?')
print(sushi_set_names)
print(len(sushi_set_names))
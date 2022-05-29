import requests
from fake_useragent import UserAgent
import json
from typing import List

def get_html_page(url: str) -> str:
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}    
    res  = requests.get(url, headers=headers)

    return res.content


def save_json(data: List[dict], file_name: str) -> None:
    with open(f'./json/{file_name}.txt', "w") as file:
        file.write(json.dumps(data))
    
import requests
import json
from typing import List
from user_agent2 import generate_user_agent


def get_html_page(url: str) -> str:
    ua = generate_user_agent(navigator="chrome")
    headers = {'User-Agent': ua}    
    res  = requests.get(url, headers=headers)

    return res.content


def save_json(data: List[dict], file_name: str) -> None:
    with open(f'./json/{file_name}.txt', "w") as file:
        file.write(json.dumps(data))
    
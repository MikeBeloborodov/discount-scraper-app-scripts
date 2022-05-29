import requests
from fake_useragent import UserAgent

def get_html_page(url: str) -> str:
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}    
    res  = requests.get(url, headers=headers)

    return res.content
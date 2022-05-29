import requests

def get_html_page(url: str, file_name: str) -> str:
    res  = requests.get(url)

    return res.text
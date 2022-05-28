import requests

def get_html_page(url: str, file_name: str) -> str:
    res  = requests.get(url)

    with open(f"{file_name}.html", "w") as file:
        file.write(res.text)
    
    return res.text
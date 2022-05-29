import json
import os
import requests
from dotenv import load_dotenv


def upload_data(url: str, email: str, password: str, all_data):
    # get token
    res = requests.get(f"{url}/login", json={"email": email, "password": password})
    acess_token = res.json()['access_token']
    
    # send data
    errors = 0
    for data in all_data:
        res = requests.post(f"{url}/promo", json=data, headers={"Authorization": f"Bearer {acess_token}"})
        if not res.status_code == 201:
            errors += 1
            print(f"[!!] ERROR WITH FILE {data['website']}")
    
    print(f"[!] DATA FINISHED UPLOADING, ERRORS - {errors}, FILES SENT - {len(all_data)}")


def delete_old_tables(url: str, email: str, password: str,):
    # get token
    res = requests.get(f"{url}/login", json={"email": email, "password": password})
    acess_token = res.json()['access_token']

    # delete tables
    res = requests.delete(f"{url}/promo", headers={"Authorization": f"Bearer {acess_token}"})
    if res.status_code == 200:
        print(f"[!] Old tables deleted")
    else:
        print(f"[!]ERROR TRYING DELETE TABLES - {res.json()}")


def main():
    try:
        os.remove('./json/all.txt')
    except:
        pass
    try:
        load_dotenv()
        URL = os.getenv('API_URL')
        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('PASSWORD')
        file_names = os.listdir("./json")
        all_jsons = []

        for file in file_names:
            with open(f"./json/{file}", "r") as json_file:
                raw = json_file.read()
                clean = json.loads(raw)
                all_jsons.extend(clean)
        with open("./json/all.txt", "w") as file:
            file.write(json.dumps(all_jsons))

        delete_old_tables(URL, EMAIL, PASSWORD)
        upload_data(URL, EMAIL, PASSWORD, all_jsons)

    except Exception as error:
        print(f"[!!] AN ERROR OCCURED DURING SENDING - {error}")
        pass

if __name__ == "__main__":
    main()
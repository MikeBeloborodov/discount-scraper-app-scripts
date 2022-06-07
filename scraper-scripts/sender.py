import json
import os
import requests
from dotenv import load_dotenv


def upload_data(all_data):
    # get token
    res = requests.get(f"{URL}/login", json={"email": EMAIL, "password": PASSWORD})
    access_token = res.json()['access_token']
    
    # send data
    errors = 0
    for data in all_data:
        res = requests.post(f"{URL}/promo", json=data, headers={"Authorization": f"Bearer {access_token}"})
        if not res.status_code == 201:
            errors += 1
            print(f"[!!] ERROR WITH FILE {data['website_title']}")
            print(res.json())
    
    print(f"[!] DATA FINISHED UPLOADING, ERRORS - {errors}, FILES SENT - {len(all_data)}")


def delete_old_tables():
    # get token
    res = requests.get(f"{URL}/login", json={"email": EMAIL, "password": PASSWORD})
    access_token = res.json()['access_token']

    # delete tables
    res = requests.delete(f"{URL}/promo", headers={"Authorization": f"Bearer {access_token}"})
    if res.status_code == 200:
        print(f"[!] Old tables deleted")
    else:
        print(f"[!]ERROR TRYING DELETE TABLES - {res.json()}")


def upload_new_websites(all_data):
    # get token
    res = requests.get(f"{URL}/login", json={"email": EMAIL, "password": PASSWORD})
    access_token = res.json()['access_token']
    
    # send data
    errors = 0
    for data in all_data:
        res = requests.post(f"{URL}/website", json=data, headers={"Authorization": f"Bearer {access_token}"})
        if not res.status_code == 201:
            errors += 1
            print(f"[!!] ERROR WITH FILE {data['website']}")
    
    print(f"[!] WEBSITES FINISHED UPLOADING, ERRORS - {errors}, WEBSITES SENT - {len(all_data)}")


def delete_old_websites():
    # get token
    res = requests.get(f"{URL}/login", json={"email": EMAIL, "password": PASSWORD})
    access_token = res.json()['access_token']

    # delete tables
    res = requests.delete(f"{URL}/website", headers={"Authorization": f"Bearer {access_token}"})
    if res.status_code == 200:
        print(f"[!] Old websites deleted")
    else:
        print(f"[!]ERROR TRYING DELETE WEBSITES - {res.json()}")


def main():
    try:
        file_names = os.listdir("./json")
        all_jsons = []
        all_websites = []

        for file in file_names:
            with open(f"./json/{file}", "r") as json_file:
                raw = json_file.read()
                clean = json.loads(raw)
                all_jsons.extend(clean)

        for file in file_names:
            with open(f"./json/{file}", "r") as json_file:
                raw = json_file.read()
                clean = json.loads(raw)
                title = clean[0]['website_title']
                link = clean[0]['website_link']
                phone_number = clean[0]['phone_number']
                category = clean[0]['category']
                all_websites.append({"title": title, "link": link, "phone_number": phone_number, "category": category})

        delete_old_tables()
        upload_data(all_jsons)
        delete_old_websites()
        upload_new_websites(all_websites)

    except Exception as error:
        print(f"[!!] AN ERROR OCCURRED DURING SENDING - {error}")
        pass


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('API_URL')
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    main()

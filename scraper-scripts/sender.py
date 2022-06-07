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
        
        with open("./old_data/all_jsons.txt", "r") as file:
            old_data_raw = file.read()
            old_data_clean = json.loads(old_data_raw)
        
        if input("Do you want to delete old tables (yes, no)? - ") == "yes":
            delete_old_tables()
        
        print(f"New data length - {len(all_jsons)}.")
        print(f"Old data length - {len(old_data_clean)}.")
        if len(all_jsons) != len(old_data_clean):
            print("Data has changed.")
        else:
            if input("Length of data is the same, do you want to check it (yes, no)? - ") == "yes":
                count = 0
                for index in range(len(all_jsons)):
                    if all_jsons[index] != old_data_clean[index]:
                        print(f"{index}-------------------")
                        print(all_jsons[index])
                        print("\n")
                        print(old_data_clean[index])
                        print("-------------------")
                        count += 1
                if count != 0:
                    print(f"Data had {count} total differences.")
                else:
                    print(f"No differences.")
        
        if input("Do you want to upload new data (yes, no)? - ") == "yes":
            upload_data(all_jsons)
        
        delete_old_websites()
        upload_new_websites(all_websites)

    except Exception as error:
        print(f"[!!] AN ERROR OCCURRED DURING SENDING")
        raise error


if __name__ == "__main__":
    load_dotenv()
    URL = os.getenv('API_URL')
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    main()

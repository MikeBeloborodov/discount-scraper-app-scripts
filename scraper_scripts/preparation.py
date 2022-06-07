import os
import json


def create_folders():
    if not os.path.exists("./json"):
        os.mkdir("json")
    
    if not os.path.exists("./html"):
        os.mkdir("html")
    
    if not os.path.exists("./old_data"):
        os.mkdir("old_data")


def save_one_json():
    json_files = os.listdir("./json")
    json_data = []

    if os.path.exists('./old_data/all_jsons.txt'):
        os.remove("./old_data/all_jsons.txt")

    for file in json_files:
        with open(f"./json/{file}", "r") as json_file:
            json_data_extracted = json.loads(json_file.read())
            json_data.extend(json_data_extracted)
    
    with open(f"./old_data/all_jsons.txt", 'w') as file:
        file.write(json.dumps(json_data))

    print("Json with total data saved.")


def delete_old_files():
    json_files = os.listdir("./json")
    html_files = os.listdir("./html")
    
    for file in json_files:
        if file == "all_jsons.txt":
            continue
        os.remove(f"./json/{file}")
    
    for file in html_files:
        os.remove(f"./html/{file}")

    print("Old files deleted.")


def main():
    try:
        create_folders()
        save_one_json()
        delete_old_files()
    except Exception as error:
        print("Error occurred while preparing")
        raise error


if __name__ == "__main__":
    main()

import os


def main():
    json_files = os.listdir("./json")
    html_files = os.listdir("./html")
    
    for file in json_files:
        os.remove(f"./json/{file}")
    
    for file in html_files:
        os.remove(f"./html/{file}")

    print("Old files deleted.")


if __name__ == "__main__":
    main()

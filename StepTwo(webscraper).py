import requests
from bs4 import BeautifulSoup
import json


# Writes application info to json file -> StepThree(data).json
def write_data(data, file="./StepThree(data).json"):
    # load the json file
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Removes HTML element information from string in array.
def convert_array_to_text(array):
    temp = []
    for item in array:
        temp.append(item.text)

    return temp


def append_data(app_title, app_link, app_desc, app_category, file='StepThree(data).json'):
    with open(file) as read_file:
        data = json.load(read_file)
        temp = data["app"]

        for item in range(len(app_title)):
            y = {"appTitle": app_title[item], "app_link": app_link[item],
                 "app_mini_description": app_desc[item], "category": app_category}
            temp.append(y)

    # Call function to write newly appended data to json file.
    write_data(data)


def read_json_file(file="stepOne(webLinks).json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data


app_store_links = read_json_file()
app_store_links = app_store_links["app_link"]

for link in app_store_links:

    item = list(link.values())[1]
    category = list(link.values())[0]

    page = requests.get(item)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='yDmH0d')

    # Class For Name: WsMG1c nnK0zc
    # Class For HREF needs https://play.google.com in front: b8cIId
    # Class For MiniDescriptions:<div class="b8cIId f5NCO">
    #
    # Find all div tags with the specified classes.
    app_title = results.find_all('div', class_='WsMG1c nnK0zc')
    app_link = []
    app_mini_description = results.find_all('div', class_='b8cIId f5NCO')

    results.find_all('div', class_='b8cIId f5NCO')

    for item in results.find_all('a', class_='mnKHRc'):
        app_link.append(item.get('href'))

    # Convert the array holding both HTML data and text data to just text data using convert function.
    app_title_text = convert_array_to_text(app_title)
    app_mini_description_text = convert_array_to_text(app_mini_description)

    # Write data to json file
    append_data(app_title_text, app_link, app_mini_description_text, category)


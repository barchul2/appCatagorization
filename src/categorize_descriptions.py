# Purpose: Categorize
import json


# Read the data from data.json file.
def read_json_data(file="./data.json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data


def append_data(list, file='./data_by_category.json'):
    with open(file) as read_file:
        data = json.load(read_file)
        temp = data["data_grouped"]

        for element in list:
            temp.append(element)

    # Call function to write newly appended data to json file.
    write_data(data)


# Writes application info to json file -> data.json
def write_data(data, file="./data_by_category.json"):
    # load the json file
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Group the data retrieved from data.json into each respective category. --> {"Category": "",
# "Descriptions":[]} written to data_by_category.json
def group_desc_by_category(data_from_file):
    app_info = data_from_file["app"]

    temp = []
    app_list = []
    for app in app_info:

        app_data = list(app.values())
        app_category = app_data[3]
        app_description = app_data[2]

        if app_category in temp:

            # Find the dictionary that contains the specific app category.
            for item in app_list:
                if item["Category"] == app_category:
                    item["app_description"].append(app_description)

        else:
            temp.append(app_category)

            # Create New dictionary to hold the category and the descriptions for that category when one
            # has not been created already.
            y = {"Category": app_category, "app_description": []}
            y["app_description"].append(app_description)
            app_list.append(y)

    print(app_list)

    # Return the completed app_list with dictionaries holding n categories ( No duplicates ) and
    # The app descriptions that belong to each category.
    return app_list


# Read data from data.json
data = read_json_data()

# Group the data by category so that all descriptions in that category are in a single list corresponding
# to a single category
categorized_data = group_desc_by_category(data)

# write the dictionaries with categories and descriptions to the data_by_category.json file
append_data(categorized_data)

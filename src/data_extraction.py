
import os
import json
import re

root_dir = '/Users/brandonarchuleta/Desktop/WebScraper/appCatagorization/src/wayne_Results/_full_results'

# Desc: This function writes data in json format to a specified json file.
# Args: Data is the text in json format to be written to the json file. File is the path to the file where the json
# data will be written.
# Output: There is no console output to this code. Output will be the written json file at the specified path.
def write_data(data, file="./wayne_results.json"):

    # load the json file as a json object and write the data to the specified file.
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Desc: This function reads json formatted data from a specified file path and returns the text data.
# Args: Data --> Path to the json file.
# Output: json object with the text of the json file.
def read_json_file(data):
    with open(data, "r") as link_file:
        data = json.load(link_file)

    return data

# Desc: This function extracts the tokens from the json format files.
# Args: Data --> The json data
# Output: A list of tokens extracted from each json file.
def extract_values(data):
    data_string = str(data["results"])
    matches = re.findall("ANDROID_APP_TOKEN\':.\'[a-zA-Z]*\'", data_string)
    temp_list = []

    for item in matches:
        temp = str(item)
        temp = temp.replace("ANDROID_APP_TOKEN", " ").replace("\'", "").replace(":","").strip()

        temp_list.append(temp)

    matches=temp_list

    # Return the list of tokens for the json file data.
    return matches


for dirname, subdirlist, fileList in os.walk(root_dir):

    # Identify the category of the results file.
    category = dirname[93:]

    # this is the identified file.
    for fname in fileList:

        # Creates the path to each results file in the directory.
        file_name = "{}/{}".format(dirname,fname)

        # Reads the text data from the results files in json format.
        text_preprocess = read_json_file(file_name)

        # Extracts tokens from the specific results file and returns them as a list.
        token_list = extract_values(text_preprocess)

        print(token_list)






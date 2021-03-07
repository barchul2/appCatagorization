# Purpose: The purpose of this script is to complete the preprocessing phase using the spacy module.
# Steps Completed can be found in the following link:
# https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f


import json
import pandas as pd
from spacy.lang.en import English

def read_json_data(file="./data.json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data

def convert_catagories_to_int(data):
    dictionaries = data['app']
    temp = []

    for dict in dictionaries:

        values_list = {"Art and Design": 1,"Augmented Reality": 2, "Auto & Vehicles": 3, "Beauty": 4,
                       "Books and Reference": 5, "Business":6, "Comics": 7, "Communication":8,
                       "Dating":9, "Daydream": 10, "Education": 11, "Entertainment": 12, "Events": 13,
                       "Finance": 14, "Food & Drink": 15, "Health & Fitness": 16, "House & Home": 17,
                       "Libraries & Demo": 18, "Lifestyle": 19, "Maps & Navigation":20, "Medical": 21,
                       "Music and Audio": 22, "Games": 23}

        for item in values_list:
            if list(dict.values())[3] == item:
                dict["category"] = values_list[item]

    return dictionaries

# Read the data from the data.json data file
data=read_json_data()

# convert the categories from text to numeric values --> Dic with number categories.
numeric_data = convert_catagories_to_int(data)

# Convert the dictionary format data to a pandas dataframe.
df = pd.DataFrame(numeric_data)






